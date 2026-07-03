"""
AGENT 4: PRD Writer
Writes the actual document. This same function is used for BOTH the first
draft AND every revision - if review_feedback exists, it writes a corrected
version instead of starting fresh.
"""
from llm import ask_text
from state import PRDState

SYSTEM_PROMPT = """You are a senior PM writing a Product Requirements Document.
Write in a clear, professional, confident tone. No vague filler language."""


def run(state: PRDState) -> PRDState:
    if state.get("review_feedback"):
        # This is a REVISION, not a first draft
        prompt = f"""Here is the current PRD draft:
{state['prd_draft']}

A Reviewer Agent found these issues:
{state['review_feedback']}

Rewrite the full PRD, fixing every issue listed. Keep everything that
was already good. Return the complete revised PRD in markdown."""
    else:
        # First draft
        prompt = f"""Requirements: {state['requirements']}
Persona: {state['persona']}
Feature Prioritization: {state['prioritization']}

Write a full PRD in markdown with these sections: Problem Statement,
Objectives, Target Users, User Stories, Functional Requirements,
Non-Functional Requirements, Success Metrics/KPIs, Risks, Timeline,
Explicitly Out of Scope."""

    prd_text = ask_text(SYSTEM_PROMPT, prompt)
    state["prd_draft"] = prd_text
    state["agent_trace"].append({
        "agent": "PRD Writer",
        "output": f"{'Revised' if state.get('review_feedback') else 'Drafted'} PRD ({len(prd_text)} chars)"
    })
    return state
