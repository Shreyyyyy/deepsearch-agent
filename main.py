import sys
import os

# Add src to the Python path
sys.path.append(os.getcwd())

from src.orchestrator import Orchestrator
from server import app  # Export app for ASGI servers like uvicorn

def main():
    """
    Main entry point for the Financial Deep Research System.
    """
    query = "Analyze the Indian IT services sector outlook"
    
    # Check if a query was provided as an argument
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])

    print(f"\n--- FINANCIAL DEEP RESEARCH SYSTEM ---\n")
    print(f"Goal: Deep investigation into '{query}'\n")

    # Step 1: Initialize System
    orchestrator = Orchestrator()

    # Step 2: User Query Understanding (Simulated)
    analysis = orchestrator.analyzer.analyze(query)
    print(f"Research Objective: {analysis['type'].capitalize()}")
    print(f"Target Sector: {analysis['sector']}")
    print(f"Research Depth: {analysis['depth']}\n")

    # Step 3: Research Planning (Simulated)
    plan = orchestrator.planner.generate_plan(query, analysis)
    print("--- RESEARCH PLAN ---\n")
    for idx, area in enumerate(plan.investigation_areas, 1):
        print(f"{idx}. {area}")
    print("\n")

    # Step 4: Execute Deep Research Loop
    # This usually takes several iterations
    print("--- STARTING DEEP RESEARCH EXECUTION ---\n")
    print(f"Looping minimum 5-10 iterations to ensure exhaustive coverage...\n")
    
    # Show the first few iterations/steps as they happen
    report = orchestrator.process_query(query)
    
    # Show detailed iterative trace
    print(orchestrator.show_research_trace()[:1000] + "...\n") # Truncated for display

    # Step 5: Final Report Generation
    print("\n--- FINAL SYNTHESIZED RESEARCH REPORT ---\n")
    print(report)

if __name__ == "__main__":
    main()
