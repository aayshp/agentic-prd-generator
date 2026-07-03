"""
AGENT 1: Requirement Gathering
Takes the raw idea, figures out what's missing, and produces structured data.
Since this runs automatically (no back-and-forth chat), it explicitly states
its own ASSUMPTIONS when something is unclear, rather than guessing silently.
"""
from llm import ask_json
from state import PRDState

SYSTEM_PROMPT = """You are a Requirement Gathering Agent on a product team.
Given a rough product idea, extract structured requirements. If something is
unclear or missing, do NOT invent confident facts - instead list it under
"assumptions" so a human can correct it later. Be specific and concrete."""


def run(state: PRDState) -> PRDState:
    output = ask_json(
        SYSTEM_PROMPT,
        f"""Product idea: {state['idea']}

Return JSON with this exact structure:
{{
  "product_name": "...",
  "core_problem": "...",
  "primary_user": "...",
  "scope": "...",
  "functional_needs": ["...", "..."],
  "assumptions": ["...", "..."],
  "open_questions": ["...", "..."]
}}"""
    )
    state["requirements"] = output
    state["agent_trace"].append({"agent": "Requirement Gathering", "output": output})
    return state
