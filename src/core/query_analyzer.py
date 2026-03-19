import json
import os
import sys
from groq import Groq

class QueryAnalyzer:
    """
    Uses LLM to dynamically analyze the user's research query.
    No more hardcoded keywords.
    """
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("GROQ_API_KEY")

    def analyze(self, query: str) -> dict:
        """
        Parses the query and returns a structured object using LLM.
        """
        if not self.api_key:
            return self._fallback_analyze(query)
            
        try:
            client = Groq(api_key=self.api_key)
            prompt = f"""Analyze the following research query for a financial analyst team.
            Query: "{query}"

            Return a RAW JSON object with:
            1. "sector": (IT, Pharma, Banking, Energy, Retail, etc. or "Cross-sector")
            2. "type": (sector analysis, company analysis, comparison, or thematic research)
            3. "depth": (Standard or Deep) 
            4. "primary_entities": List of names of companies or organizations mentioned.
            5. "intent": Describe the core analytical goal in one sentence.
            """
            
            completion = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile",
                response_format={"type": "json_object"}
            )
            return json.loads(completion.choices[0].message.content)
        except Exception as e:
            print(f"LLM Analysis failed: {e}")
            return self._fallback_analyze(query)

    def _fallback_analyze(self, query: str) -> dict:
        query_lower = query.lower()
        sector = "Cross-sector"
        if "it" in query_lower or "software" in query_lower: sector = "IT"
        if "pharma" in query_lower or "drug" in query_lower: sector = "Pharma"
        
        return {
            "query": query,
            "sector": sector,
            "type": "sector analysis",
            "depth": "Standard",
            "primary_entities": [],
            "intent": "Research based on keywords."
        }
