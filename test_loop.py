import os
import sys
from dotenv import load_dotenv

load_dotenv()
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.query_analyzer import QueryAnalyzer
from src.core.research_planner import ResearchPlanner
from src.core.research_executor import ResearchExecutor
from src.core.financial_analysis import FinancialAnalysisModule
from src.core.report_generator import ReportGenerator

def test_full_loop():
    query = "oil condition in india right now"
    api_key = os.getenv("GROQ_API_KEY")
    print(f"API Key: {api_key[:10]}...")
    
    analyzer = QueryAnalyzer(api_key=api_key)
    planner = ResearchPlanner(api_key=api_key)
    executor = ResearchExecutor(api_key=api_key)
    financial = FinancialAnalysisModule(api_key=api_key)
    report_gen = ReportGenerator(api_key=api_key)

    # 1. Analyze
    analysis = analyzer.analyze(query)
    print("Analysis:", analysis)
    
    # 2. Plan
    plan = planner.generate_plan(query, analysis)
    print("Plan Investigation Areas:", plan.investigation_areas)
    
    # 3. Execute (single step for testing)
    # We mock executor to just return one result to avoid long time
    executor.findings = [{"title": "Test Result", "content": "The oil condition in India is complex with recent price shifts. Brent crude is trading at...", "source": "Reuters"}]
    executor.reasoning_trace = [{"step": 1, "label": "Initial Research", "queries_executed": [query], "insights_found": ["Price shifts"], "reasoning": "Need more context."}]
    
    # 4. Extract
    kpis = financial.extract_and_compute(executor.findings)
    print("KPIs:", kpis)
    
    # 5. Synthesis
    report = report_gen.generate(plan, executor, kpis)
    print("Report synthesized successfully (first 100 chars):", report[:100])

if __name__ == "__main__":
    test_full_loop()
