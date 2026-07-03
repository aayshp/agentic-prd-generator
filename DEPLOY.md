# Deploying Your Agentic PRD Generator (No Terminal Needed)

This gets you a real, live website link — the kind you post on LinkedIn and
people can actually click and use. Everything below happens in your browser.

## Part 1 — Put the code on GitHub (browser only)

1. Go to github.com, sign up/log in (free)
2. Click the "+" top right -> "New repository"
3. Name it something like `agentic-prd-generator`, keep it Public, click Create
4. On the new repo page, click "uploading an existing file"
5. Drag in EVERY file and folder from the `agentic-prd-generator` folder I gave
   you (app.py, graph.py, requirements.txt, the whole `agents` folder, README)
6. Scroll down, click "Commit changes"

That's it — your code now lives on GitHub. No git commands, no terminal.

## Part 2 — Deploy it live (browser only)

1. Go to share.streamlit.io, sign in with your GitHub account
2. Click "Create app" -> "From existing repo"
3. Pick your `agentic-prd-generator` repo, set Main file path to `app.py`
4. Click "Advanced settings" -> "Secrets" and paste this in:
   ```
   GROQ_API_KEY = "your-actual-groq-key-here"
   ```
5. Click "Deploy"

Wait ~2-3 minutes. You'll get a live URL like:
`https://your-app-name.streamlit.app`

That link is real, live, and works for anyone who clicks it — no login needed
for them to try it.

## Part 3 — What to actually post on LinkedIn

Don't just post the link. Show the THING that makes it interesting:

- **Screen-record yourself using it** (Loom, or just your phone recording
  your screen) — type an idea, show the "agent trace" tab expanding to
  reveal each agent's work, show the Reviewer sending it back for revision.
  That loop happening ON SCREEN is the proof this isn't just one AI prompt.
- **Post 2-3 screenshots**: the input box, the agent trace expanded, the
  final PRD. Before/after (draft vs. reviewed) is a great visual if you
  still have the Apex Pharma draft1 vs final files.
- **In the caption**, name the actual architecture in plain words: "Built
  as a 5-agent pipeline using LangGraph — Requirement Gathering → Persona
  → Feature Prioritization → PRD Writer → Reviewer, with the Reviewer
  agent sending work back for revision until it passes quality review."
  That sentence alone signals "system," not "prompt," to anyone technical
  reading it.
- **Link the live app AND the GitHub repo** — recruiters and PMs will click
  the app, engineers will click the repo.

## If something breaks during deploy

Streamlit's deploy logs will show you the exact error — usually a missing
package in requirements.txt. Paste the error back to me and I'll fix the
file directly.
