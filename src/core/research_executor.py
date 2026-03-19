import time
from typing import List, Dict, Generator
import json
import os
import re
from duckduckgo_search import DDGS
import trafilatura
from bs4 import BeautifulSoup
import requests

class ResearchExecutor:
    """
    Real-world research executor that performs web searching, scraping,
    and analysis.
    """
    def __init__(self, api_key: str = None):
        self.max_steps = 10
        self.reasoning_trace = []
        self.findings = []
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
        }

    def execute_streaming(self, plan, depth: str = "Standard") -> Generator[Dict, None, None]:
        if depth == "Deep":
            self.max_steps = 15

        step_map = self._build_dynamic_step_map(plan)
        
        for step_idx, (step_label, queries, action) in enumerate(step_map, 1):
            if step_idx > self.max_steps: break
            
            yield {
                "type": "step_start",
                "step": step_idx,
                "label": step_label,
                "action": action,
                "queries": queries
            }

            step_findings = []
            for q in queries:
                yield {"type": "thought", "message": f"Trying search query: '{q}'...", "level": "info"}
                
                try:
                    search_results = self._real_search(q)
                    scrape_count = 0
                    for res in search_results[:5]: 
                        if scrape_count >= 2: break
                        
                        url = res.get('href')
                        title = res.get('title')
                        if not url: continue
                        
                        yield {"type": "thought", "message": f"Extracting: {title[:40]}...", "level": "info"}
                        
                        raw_content = self._real_scrape(url)
                        if not raw_content or len(raw_content) < 200:
                            continue
                        
                        yield {"type": "thought", "message": f"Analyzing {title[:40]}...", "level": "info"}
                        
                        analysis = self._perform_llm_analysis(q, raw_content[:15000], title)
                        if analysis and analysis.get("content"):
                            # ALWAYS ATTACH REAL URL
                            analysis["url"] = url 
                            step_findings.append(analysis)
                            scrape_count += 1
                            yield {
                                "type": "thought",
                                "message": f"Insight Extracted: {analysis.get('title', 'Fact Extracted')}",
                                "level": "success"
                            }
                except Exception as e:
                    yield {"type": "thought", "message": f"Agent Error: {str(e)}", "level": "error"}

            self.findings.extend(step_findings)
            self.reasoning_trace.append({
                "step": step_idx,
                "label": step_label,
                "queries_executed": queries,
                "insights_found": [f["title"] for f in step_findings],
                "reasoning": f"Exploration of {step_label} concluded with {len(step_findings)} insights."
            })

            yield {
                "type": "step_done",
                "step": step_idx,
                "label": step_label,
                "insights": [f["title"] for f in step_findings],
                "reasoning": f"Gathered total {len(step_findings)} intelligence points in this phase."
            }

    def _real_search(self, query: str) -> List[Dict]:
        all_res = []
        try:
            with DDGS() as ddgs:
                try:
                    res_news = list(ddgs.news(query, max_results=10))
                    all_res.extend([{"title": r['title'], "href": r['url']} for r in res_news])
                except: pass
                
                if len(all_res) < 3:
                    try:
                        res_text = list(ddgs.text(query, max_results=10))
                        all_res.extend([{"title": r['title'], "href": r['href']} for r in res_text])
                    except: pass
            return all_res
        except Exception as e:
            return []

    def _real_scrape(self, url: str) -> str:
        try:
            downloaded = trafilatura.fetch_url(url)
            if downloaded:
                result = trafilatura.extract(downloaded, include_tables=True)
                if result and len(result) > 300:
                    return result
        except: pass

        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                for script in soup(["script", "style"]):
                    script.decompose()
                text = soup.get_text(separator=' ')
                lines = (line.strip() for line in text.splitlines())
                chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                text = '\n'.join(chunk for chunk in chunks if chunk)
                if len(text) > 300:
                    return text
        except: pass
        return None

    def _perform_llm_analysis(self, query: str, content: str, source_title: str) -> Dict:
        if self.api_key:
            return self._call_groq_llm(query, content, source_title)
        else:
            return self._fallback_analyzer(query, content, source_title)

    def _call_groq_llm(self, query: str, content: str, source_title: str) -> Dict:
        try:
            from groq import Groq
            client = Groq(api_key=self.api_key)
            prompt = f"""
            Analyze source: {source_title} for query: "{query}"
            Content: {content[:10000]}
            Return RAW JSON:
            - "title": string
            - "content": detailed facts synthesis
            - "metrics": dict of numbers
            """
            chat_completion = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile",
                response_format={"type": "json_object"}
            )
            return json.loads(chat_completion.choices[0].message.content)
        except Exception as e:
            return self._fallback_analyzer(query, content, source_title)

    def _fallback_analyzer(self, query: str, content: str, source_title: str) -> Dict:
        text = content[:2000]
        numbers = re.findall(r'\d+\.?\d*[\%kmbKM B\$]', text)
        return {
            "title": f"Source: {source_title[:40]}",
            "content": f"Found metrics: {', '.join(set(numbers))[:100]}",
            "metrics": {"found_numbers": list(set(numbers))[:5]}
        }

    def _build_dynamic_step_map(self, plan) -> List:
        areas = plan.investigation_areas
        questions = plan.questions
        steps = []
        for i, area in enumerate(areas):
            q_per_area = max(1, len(questions) // len(areas))
            start = i * q_per_area
            end = (i + 1) * q_per_area if i < len(areas) - 1 else len(questions)
            step_queries = questions[start:end]
            if not step_queries: step_queries = [f"{area} trends 2026 {plan.query}"]
            steps.append((area, step_queries, f"🔍 Deep Dive: {area}"))
        return steps
