import json
import asyncio
from typing import AsyncGenerator, Dict
import os
import sys

# Load env before everything
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, StreamingResponse
from pydantic import BaseModel

# Add src to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.query_analyzer import QueryAnalyzer
from src.core.research_planner import ResearchPlanner
from src.core.research_executor import ResearchExecutor
from src.core.financial_analysis import FinancialAnalysisModule
from src.core.report_generator import ReportGenerator
from src.agents.base_agent import ITAgent, PharmaAgent

app = FastAPI(title="DeepResearch Intel Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Sector Registry (Fallback/Heuristics)
SECTOR_AGENTS = {
    "IT": ITAgent(),
    "Pharma": PharmaAgent()
}

@app.get("/api/research/stream")
async def stream_research(query: str):
    """
    Server-Sent Events endpoint - streams research steps live to the chat UI.
    Now with DYNAMIC Planning and AI Synthesis.
    """
    async def event_generator() -> AsyncGenerator[str, None]:
        api_key = os.getenv("GROQ_API_KEY")
        
        try:
            # Step 1: Initialize CORE
            # All core modules are now LLM-ENABLED
            analyzer = QueryAnalyzer(api_key=api_key)
            planner = ResearchPlanner(api_key=api_key)
            executor = ResearchExecutor(api_key=api_key)
            financial = FinancialAnalysisModule(api_key=api_key)
            report_gen = ReportGenerator(api_key=api_key)

            # --- Step 1: Dynamic Query Analysis ---
            yield _sse_event("analysis", {"message": "Diving into query semantics..."})
            analysis = analyzer.analyze(query)
            sector = analysis.get("sector", "Cross-sector")
            yield _sse_event("analysis", {
                "sector": sector,
                "type": analysis.get("type", "Deep Dive"),
                "depth": analysis.get("depth", "Standard"),
                "message": f"Target identified: **{sector} Intelligence Unit**."
            })
            await asyncio.sleep(0.5)

            # --- Step 2: Dynamic Planning ---
            yield _sse_event("plan", {"message": "Building research strategy..."})
            plan = planner.generate_plan(query, analysis)
            
            # Allow Sector Agents to refine (optional heuristics)
            agent = SECTOR_AGENTS.get(sector)
            if agent:
                plan = agent.refine_plan(plan)

            yield _sse_event("plan", {
                "areas": plan.investigation_areas,
                "questions": plan.questions[:10],
                "sources": plan.sources,
                "message": f"Strategy locked with **{len(plan.investigation_areas)} investigation dimensions**."
            })
            await asyncio.sleep(0.4)

            # --- Step 3: Progressive Deep Research ---
            yield _sse_event("research_start", {
                "message": "Initializing Deep Research Loop..."
            })
            
            # Start streaming research loop events
            # This handles searching + scraping + LLM micro-analysis
            for event in executor.execute_streaming(plan, analysis.get("depth", "Standard")):
                yield _sse_event(event["type"], event)
                await asyncio.sleep(0.1)

            # --- Step 4: Metric Extraction ---
            yield _sse_event("financial_start", {"message": "Synthesizing KPIs from gathered raw intelligence..."})
            kpis = financial.extract_and_compute(executor.findings)
            yield _sse_event("financial_done", {"kpis": kpis})
            await asyncio.sleep(0.3)

            # --- Step 5: Final Report Synthesis ---
            yield _sse_event("report_start", {"message": f"Synthesizing final high-fidelity report from **{len(executor.findings)} sources**..."})
            report = report_gen.generate(plan, executor, kpis)
            
            yield _sse_event("report", {
                "content": report,
                "steps": len(executor.reasoning_trace),
                "message": "Deep Research session complete."
            })

            yield _sse_event("done", {"message": "End of session."})

        except Exception as e:
            import traceback
            traceback.print_exc()
            yield _sse_event("error", {"message": f"Research interrupted: {str(e)}"})

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive"}
    )

def _sse_event(event_type: str, data: dict) -> str:
    return f"event: {event_type}\ndata: {json.dumps(data)}\n\n"

@app.get("/", response_class=HTMLResponse)
async def serve_ui():
    try:
        with open(os.path.join(os.path.dirname(__file__), "ui", "index.html"), "r") as f:
            return HTMLResponse(content=f.read())
    except Exception as e:
        return HTMLResponse(content=f"Error loading UI: {e}", status_code=500)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
