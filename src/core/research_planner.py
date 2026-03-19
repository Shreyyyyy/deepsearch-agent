import json
import os
from typing import List, Dict
from groq import Groq

class ResearchPlan:
    def __init__(self, query: str, sector: str, type_: str):
        self.query = query
        self.sector = sector
        self.type = type_
        self.investigation_areas = []
        self.questions = []
        self.sources = ["Web search", "Financial filings (RAG)", "Market data APIs"]

class ResearchPlanner:
    """
    Generates a dynamic research plan based on the analyzed query using an LLM.
    No more sector-specific templates.
    """
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("GROQ_API_KEY")

    def generate_plan(self, query: str, analysis: dict) -> ResearchPlan:
        """
        Dynamically plan research by asking the LLM to identify the 5-7 most critical
        areas of investigation for this query.
        """
        plan = ResearchPlan(query, analysis.get("sector", "Cross-sector"), analysis.get("type", "sector analysis"))
        
        if not self.api_key:
            return self._fallback_plan(query, analysis)

        try:
            client = Groq(api_key=self.api_key)
            prompt = f"""Generate a research plan for a professional financial analyst for the following query:
            
            Query: "{query}"
            Sector: {analysis['sector']}
            Entities: {analysis['primary_entities']}

            Return a RAW JSON object with:
            1. "investigation_areas": (At least 5 distinct areas, e.g. Market share, Margin pressures, Pipeline, Regulatory risk, etc.)
            2. "questions": (At least 7 specific, data-oriented search queries to answer those areas)
            3. "sources": (Target data sources like Annual reports, USFDA logs, NASSCOM, etc.)
            """
            
            completion = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile",
                response_format={"type": "json_object"}
            )
            data = json.loads(completion.choices[0].message.content)
            
            plan.investigation_areas = data.get("investigation_areas", [])
            plan.questions = data.get("questions", [])
            plan.sources = data.get("sources", ["Web", "Reports"])
            return plan

        except Exception as e:
            print(f"Planning failed: {e}")
            return self._fallback_plan(query, analysis)

    def _fallback_plan(self, query: str, analysis: dict) -> ResearchPlan:
        plan = ResearchPlan(query, analysis.get("sector"), analysis.get("type"))
        plan.investigation_areas = ["Market Sentiment", "Competitive Positioning", "Financial Performance"]
        plan.questions = [query, f"Latest news on {analysis.get('sector')} sector", f"Financial reports for top firms in {analysis.get('sector')}"]
        return plan
