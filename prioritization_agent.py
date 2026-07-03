"""
AGENT 3: Feature Prioritization
Sorts requirements into Must/Should/Could/Won't-have using MoSCoW, so the
PRD Writer knows what's MVP vs future roadmap.
"""
from llm import ask_json
from state import PRDState

SYSTEM_PROMPT = """You are a Feature Prioritization Agent on a product team.
Using the MoSCoW method, sort features into Must-have, Should-have,
Could-have, and Won't-have (this round). Be decisive - a real MVP cannot
have everything as "Must-have"."""


def run(state: PRDState) -> PRDState:
    output = ask_json(
        SYSTEM_PROMPT,
        f"""Requirements: {state['requirements']}
Persona: {state['persona']}

Return JSON with this exact structure:
{{
  "must_have": ["...", "..."],
  "should_have": ["...", "..."],
  "could_have": ["...", "..."],
  "wont_have_this_round": ["...", "..."]
}}"""
    )
    state["prioritization"] = output
    state["agent_trace"].append({"agent": "Feature Prioritization", "output": output})
    return state
