import json
import os
from typing import List, Dict
from groq import Groq

class ReportGenerator:
    """
    Final synthesis and report formatting using an LLM.
    STRICT: Sources MUST be clickable Markdown links.
    """
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("GROQ_API_KEY")

    def generate(self, plan: 'ResearchPlan', executor: 'ResearchExecutor', analysis_kpis: Dict) -> str:
        """
        Final synthesis of all research.
        """
        if not self.api_key:
            return self._fallback_synthesis(plan, executor, analysis_kpis)

        try:
            client = Groq(api_key=self.api_key)
            evidence = [f for f in executor.findings if f.get("content")]
            
            # ATTACH REAL URLs FOR THE LLM
            evidence_text = "\n\n".join([
                f"SOURCE_TITLE: {f.get('title', 'Unknown')}\n"
                f"URL: {f.get('url', '#')}\n"
                f"INSIGHT: {f['content']}\n"
                f"METRICS: {str(f.get('metrics', {}))}"
                for f in evidence[:12]
            ])
            
            trace_text = "\n".join([f"Step {t['step']} ({t['label']}): {t['reasoning']}" for t in executor.reasoning_trace])
            
            prompt = f"""WRITE A HIGH-QUALITY FINANCIAL RESEARCH REPORT.
            QUERY: "{plan.query}"
            SECTOR: {plan.sector}
            INVESTIGATION AREAS: {plan.investigation_areas}
            
            GATHERED EVIDENCE (MANDATORY: LINK TO THESE):
            ---
            {evidence_text}
            ---
            
            FINANCIAL KPIs:
            {analysis_kpis}

            STRICT FORMATTING RULE:
            - Every time you mention a finding or in the 'Sources & Audit Trace' section, you MUST format the source as a CLICKABLE MARKDOWN LINK.
            - Format: [Source Title](URL)
            - Example: [Reuters Market Report](https://reuters.com/...)
            - If URL is missing, use the Source Title as plain text.

            Structure: Title, Executive Summary, Deep Research Insights, Consolidated Data Table, Outlook & Risks, and Sources & Audit Trace (with LINKS).
            TONE: Professional Analyst. High-quality Markdown.
            """
            
            completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a senior analyst. Every source mentioned MUST be a clickable markdown link [Title](URL)."},
                    {"role": "user", "content": prompt}
                ],
                model="llama-3.3-70b-versatile",
            )
            return completion.choices[0].message.content

        except Exception as e:
            print(f"CRITICAL: Report synthesis failed with error: {e}")
            return self._fallback_synthesis(plan, executor, analysis_kpis)

    def _fallback_synthesis(self, plan, executor, analysis_kpis) -> str:
        return f"# Intelligence Report: {plan.query}\n\nSynthesis error. Critical logs may contain details."
