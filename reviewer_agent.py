"""
AGENT 5: Reviewer / Critic
Acts like a skeptical senior PM. Reads the PRD draft and decides: good
enough to ship, or send back for revision? This is the node that makes
the whole thing a LOOP instead of a straight line.
"""
from llm import ask_json
from state import PRDState

SYSTEM_PROMPT = """You are a skeptical Senior PM reviewing a PRD written by
a junior colleague. Look specifically for: missing baseline numbers,
unfilled placeholders (like "TBD" with no plan), contradictions between
sections, missing ownership, and scope creep. Be genuinely critical - don't
approve mediocre work.

IMPORTANT: The PRD must keep its existing 10 sections exactly as they are
(Problem Statement, Objectives, Target Users, User Stories, Functional
Requirements, Non-Functional Requirements, Success Metrics/KPIs, Risks,
Timeline, Explicitly Out of Scope). Do NOT suggest adding new sections
(like a RACI chart, appendix, or glossary) - flag issues WITHIN the
existing sections only. Keep feedback to at most 4 issues so revisions
stay focused and don't balloon in length.

ALSO CHECK: any specific number, percentage, or metric in the PRD that
looks invented (not explicitly given by the user) must be labeled
"(ASSUMED - validate with real data before use)". If you find a precise
number without that label, flag it as an issue - presenting a made-up
number as real data is a serious problem, not a minor one.

ALSO CHECK: any owner/lead field with an invented named individual (e.g.
"Priya Singh", "John Doe") instead of a team/role name. Flag this as an
issue too - fabricated employee names are misleading."""

MAX_REVISIONS = 2  # safety limit so the loop can't run forever


def run(state: PRDState) -> PRDState:
    output = ask_json(
        SYSTEM_PROMPT,
        f"""PRD Draft:
{state['prd_draft']}

Return JSON with this exact structure:
{{
  "quality_score": <number 1-10>,
  "issues": ["specific issue 1", "specific issue 2"],
  "approved": <true or false - true only if quality_score is 8 or higher>
}}"""
    )
    state["review_feedback"] = output
    state["revision_count"] += 1

    # Approve if reviewer says so, OR if we've hit the safety limit
    state["is_approved"] = output.get("approved", False) or state["revision_count"] >= MAX_REVISIONS

    state["agent_trace"].append({"agent": "Reviewer", "output": output})
    return state


def should_revise(state: PRDState) -> str:
    """This is the conditional edge - decides where the graph goes next."""
    return "end" if state["is_approved"] else "revise"
