from abc import ABC, abstractmethod
from typing import List, Dict

class BaseAgent(ABC):
    """
    Abstract base class for all sector-specific research agents.
    Allows for domain-specific heuristics to refine dynamic plans.
    """
    def __init__(self, sector: str):
        self.sector = sector

    def refine_plan(self, plan: 'ResearchPlan') -> 'ResearchPlan':
        """
        By default, adds sector-specific depth if not present.
        """
        return plan

class ITAgent(BaseAgent):
    def __init__(self):
        super().__init__("IT")

    def refine_plan(self, plan: 'ResearchPlan') -> 'ResearchPlan':
        # Add tech-specific depth
        if "GenAI" not in str(plan.investigation_areas):
            plan.investigation_areas.append("GenAI Implementation & Monetization")
        return plan

class PharmaAgent(BaseAgent):
    def __init__(self):
        super().__init__("Pharma")

    def refine_plan(self, plan: 'ResearchPlan') -> 'ResearchPlan':
        # Add pharma-specific regulatory depth
        if "USFDA" not in str(plan.investigation_areas):
            plan.investigation_areas.append("USFDA Regulatory Compliance History")
        return plan
