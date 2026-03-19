from src.core.query_analyzer import QueryAnalyzer
from src.core.research_planner import ResearchPlanner, ResearchPlan
from src.core.research_executor import ResearchExecutor
from src.core.financial_analysis import FinancialAnalysisModule
from src.core.report_generator import ReportGenerator
from src.agents.base_agent import ITAgent, PharmaAgent

class Orchestrator:
    """
    Main entry point for the Financial Deep Research System.
    Routes queries to the correct sector agent and handles the overall workflow.
    """
    def __init__(self):
        self.analyzer = QueryAnalyzer()
        self.planner = ResearchPlanner("Generic")
        self.executor = ResearchExecutor()
        self.financial_analyst = FinancialAnalysisModule()
        self.report_gen = ReportGenerator()
        
        # Sector Registry
        self.sector_agents = {
            "IT": ITAgent(),
            "Pharma": PharmaAgent()
        }

    def process_query(self, query: str) -> str:
        """
        Step-by-step processing of a research request.
        """
        # Step 1: Query Understanding
        analysis = self.analyzer.analyze(query)
        sector_name = analysis["sector"]
        depth = analysis["depth"]
        
        # Polite Rejection for non-financial queries (Simplified)
        if sector_name == "Unknown":
            return "I am a financial research analyst. I can only help with queries related to IT or Pharma sectors."

        # Step 2: Routing to correct Sector Agent
        agent = self.sector_agents.get(sector_name)
        
        # Step 3: Research Planning (Generic + Sector Refined)
        plan = self.planner.generate_plan(query, analysis)
        if agent:
            plan = agent.refine_plan(plan)
            
        # Step 4: Iterative Deep Research Execution
        findings = self.executor.execute(plan, depth)
        
        # Step 5: Financial Analysis Module (Calculations)
        kpis = self.financial_analyst.extract_and_compute(findings)
        
        # Step 6: Synthesis and Report Generation
        report = self.report_gen.generate(plan, self.executor, kpis)
        
        return report

    def show_research_trace(self) -> str:
        """
        Returns the iterative reasoning trace from the executor.
        """
        trace_str = "# Iterative Research Reasoning Trace\n"
        for trace in self.executor.reasoning_trace:
            trace_str += f"**Step {trace['step']}**:\n"
            trace_str += f"- Queries: {', '.join(trace['queries_executed'][:20])}\n"
            trace_str += f"- Findings: {', '.join(trace['insights_found'])}\n"
            trace_str += f"- Reasoning: {trace['reasoning']}\n\n"
        return trace_str
