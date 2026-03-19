import json
import os
import re
from typing import Dict, List, Optional
from groq import Groq

class FinancialAnalysisModule:
    """
    Synthesizes financial KPIs from all collected research insights.
    Replaces simulated KPIs with LLM-led extraction of real metrics.
    """
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("GROQ_API_KEY")

    def extract_and_compute(self, insights: List[Dict]) -> Dict:
        """
        Takes all findings from the research executor and asks the LLM
        to identify and structure key metrics/KPIs gathered.
        """
        if not self.api_key:
            return self._fallback_kpis()

        try:
            client = Groq(api_key=api_key)
            # We focus on the most data-rich findings
            all_text = "\n\n".join([
                f"Source: {i['title']}\n"
                f"Data Snapshot: {str(i['content'])[:500]}\n"
                f"Metrics Found: {str(i.get('metrics', {}))}" 
                for i in insights[:15]
            ])
            
            prompt = f"""
            Identify and structure exact financial KPIs, percentages, and dollar amounts from the research findings.
            
            Findings: 
            {all_text}

            Return a RAW JSON object with:
            - "growth": (A primary growth percentage, e.g. "CAGR: 12.5% (2023-2026)")
            - "margins": (A primary profitability metric found, e.g. "EBITDA Margin: 21%")
            - "cashflow_ratios": (Any ratio related to cash or liquidity)
            - "sector_kpis": (At least 5 distinct key metrics/data points found in findings)
            """
            
            completion = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile",
                response_format={"type": "json_object"}
            )
            data = json.loads(completion.choices[0].message.content)
            
            return {
                "growth": data.get("growth", "Not reported in findings"),
                "margins": data.get("margins", "Not reported in findings"),
                "cashflow_ratios": data.get("cashflow_ratios", "Not reported in findings"),
                "sector_kpis": data.get("sector_kpis", {"Finding": "No hard KPIs detected in scrape."})
            }

        except Exception as e:
            print(f"Extraction failed: {e}")
            return self._fallback_kpis()

    def _fallback_kpis(self) -> Dict:
        return {
            "growth": "N/A (Extraction Error)",
            "margins": "N/A (Extraction Error)",
            "cashflow_ratios": "N/A",
            "sector_kpis": {"Error": "Financial extraction failed."}
        }
