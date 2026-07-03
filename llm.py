"""
One shared connection to Groq, used by every agent. Keeping this in one
place means if we ever switch models or providers, we change it once.
"""
import os
import json
from langchain_groq import ChatGroq

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    api_key=os.environ.get("GROQ_API_KEY"),
    temperature=0.4,
)


def ask_json(system_prompt: str, user_prompt: str) -> dict:
    """
    Sends a prompt, asks for JSON back, parses it safely.
    Every agent that needs structured (not free-text) output uses this.
    """
    response = llm.invoke([
        {"role": "system", "content": system_prompt + "\nRespond ONLY with valid JSON. No markdown, no preamble."},
        {"role": "user", "content": user_prompt},
    ])
    text = response.content.strip()
    # Strip accidental markdown fences if the model adds them anyway
    if text.startswith("```"):
        text = text.strip("`")
        text = text.replace("json\n", "", 1)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {"raw_output": text, "parse_error": True}


def ask_text(system_prompt: str, user_prompt: str) -> str:
    """For agents that just need to write prose (like the PRD Writer)."""
    response = llm.invoke([
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ])
    return response.content
