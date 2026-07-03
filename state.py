"""
The SHARED STATE - this is the data object that gets passed from agent to
agent. Each agent reads what it needs from this and adds its own piece to it.
Think of it as a shared notebook the whole team writes into.
"""
from typing import TypedDict, List, Dict, Optional


class PRDState(TypedDict):
    idea: str                          # raw input from the user
    requirements: Dict                 # output of Requirement Agent
    persona: Dict                      # output of Persona Agent
    prioritization: Dict               # output of Prioritization Agent
    prd_draft: str                     # current PRD text (gets overwritten each revision)
    review_feedback: Optional[Dict]    # Reviewer Agent's latest critique
    revision_count: int                # how many times we've looped
    is_approved: bool                  # did the Reviewer sign off?
    agent_trace: List[Dict]            # log of what each agent did, for the UI to show
