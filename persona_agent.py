"""
AGENT 2: Persona Generation
Reads the structured requirements and builds a realistic user persona with
pain points and a Job To Be Done (JTBD).
"""
from llm import ask_json
from state import PRDState

SYSTEM_PROMPT = """You are a Persona Generation Agent on a product team.
Given structured product requirements, create a realistic primary persona
with genuine pain points, a Job To Be Done, and a real usage scenario."""


def run(state: PRDState) -> PRDState:
    output = ask_json(
        SYSTEM_PROMPT,
        f"""Requirements: {state['requirements']}

Return JSON with this exact structure:
{{
  "persona_name": "...",
  "role": "...",
  "pain_points": ["...", "..."],
  "jtbd": "...",
  "scenario": "..."
}}"""
    )
    state["persona"] = output
    state["agent_trace"].append({"agent": "Persona Generation", "output": output})
    return state
