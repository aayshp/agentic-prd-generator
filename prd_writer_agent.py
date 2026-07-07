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
was already good. Keep the "Prepared by" line exactly as it currently is,
do not change the name, and do not duplicate it elsewhere.

Also re-check these rules while revising - fix any violations even if the
Reviewer didn't explicitly mention them:
- Every specific number must end with "(ASSUMED - validate with real data
  before use)" - no exceptions.
- No invented named individuals anywhere (owner/lead fields must use team
  or role names only, e.g. "Data Engineering Team").

Return the complete revised PRD in markdown."""
    else:
        # First draft
        author = state.get("author_name") or "Product Manager"
        prompt = f"""Requirements: {state['requirements']}
Persona: {state['persona']}
Feature Prioritization: {state['prioritization']}

Write a full PRD in markdown with EXACTLY these sections, in this order, and
no other sections: Problem Statement, Objectives, Target Users, User Stories,
Functional Requirements, Non-Functional Requirements, Success Metrics/KPIs,
Risks, Timeline, Explicitly Out of Scope.

=== CRITICAL RULE 1: DATA HONESTY (no exceptions) ===
You were only given a product idea, not real company data. This means you
have ZERO real numbers to work with. EVERY specific number, percentage,
duration, or dollar figure you write (spike counts, downtime hours, cost
estimates, latency targets, failure rates, baseline metrics - anything with
a digit in it) MUST end with "(ASSUMED - validate with real data before use)".
No number is exempt from this, including ones in tables.

Correct example: "Factory lines generate approximately 12 energy spikes
per week (ASSUMED - validate with real data before use)."
Incorrect (do NOT do this): "Factory lines generate approximately 12
energy spikes per week."

If a table has many numbers, you may add ONE footnote instead of repeating
the tag on every cell, but only if you place it directly under the table:
"*All figures in this table are placeholders (ASSUMED - validate with real
data before use).*"

=== CRITICAL RULE 2: NO INVENTED PEOPLE ===
Do NOT invent named individuals (e.g. "Priya Singh", "John Doe", "Luis
Martínez") for owner/lead/team fields anywhere in the document, including
Functional Requirements, Risks, and Timeline tables. Real employee names
don't exist yet for this hypothetical company. Use team or role names only
(e.g. "Data Engineering Team", "QA Lead - name TBD", "Security Team").
The ONLY real name allowed anywhere in this document is the author,
{author}, and only in the "Prepared by" line.

=== CRITICAL RULE 3: NO DUPLICATE HEADERS ===
Do not repeat "Prepared by" or "Date" anywhere except the top of the
document. Do not add a second author line at the end.

For User Stories: write 4-6 stories max, each in the exact format
"As a [specific role], I want [specific capability], so that [specific
benefit]." Keep each one to one sentence. Do not add sub-bullets, acceptance
criteria, or extra detail under each story - that belongs in Functional
Requirements instead.

At the very top, include:
Product: [a short product name you choose]
Prepared by: {author}
Date: [today's date]

Do NOT invent or use any other name for "Prepared by" - use exactly: {author}"""

    prd_text = ask_text(SYSTEM_PROMPT, prompt)
    state["prd_draft"] = prd_text
    state["agent_trace"].append({
        "agent": "PRD Writer",
        "output": f"{'Revised' if state.get('review_feedback') else 'Drafted'} PRD ({len(prd_text)} chars)"
    })
    return state
