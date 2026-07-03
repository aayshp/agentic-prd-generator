# Agentic PRD Generator

Not a "type an idea, get a PRD" tool. A system that works through the PRD like
an actual product team would — gathering requirements, checking competitors,
building personas, prioritizing features, writing the doc, then critiquing
and revising it before calling it done.

## Why this exists

Most PRD generators are:

```
Input -> LLM -> PRD Output
```

This one is:

```
Input -> Requirement Gathering Agent -> Competitor Intelligence Agent
      -> Persona Agent -> Feature Prioritization Agent -> PRD Writer Agent
      -> Reviewer Agent -> (loop back to PRD Writer if issues found) -> Final PRD
```

## Build order (this is the actual plan — follow it in order, don't skip ahead)

- [x] **Step 1** — `step1_basic_prd.py`: dumb baseline, one LLM call, no agents.
      This exists purely as a comparison point and a sanity check that the
      API key/setup works.
- [ ] **Step 2** — Requirement Gathering Agent, built and tested alone.
      Takes a rough idea, asks clarifying questions, outputs structured JSON.
- [ ] **Step 3** — PRD Writer Agent, built and tested alone (fed fake/hand-written
      structured data to start, since the other agents don't exist yet).
- [ ] **Step 4** — Connect Step 2 -> Step 3 for real. First real pipeline.
- [ ] **Step 5** — Plug in the existing Competitor Intelligence agent, then build
      Persona Agent and Feature Prioritization Agent the same way: one at a
      time, tested alone, then connected.
- [ ] **Step 6** — Reviewer Agent + the revision loop (hardest part, saved for
      last on purpose — loops are much harder to debug than a straight line).
- [ ] **Step 7** — Company style adaptation (upload past PRDs, match tone/structure),
      swap Streamlit for Next.js if needed, decide on Pinecone vs Chroma at scale.

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env   # then fill in your OPENAI_API_KEY
export OPENAI_API_KEY="your-key-here"   # or use python-dotenv to load .env
python step1_basic_prd.py
```

## Folder structure

```
agentic-prd-generator/
├── step1_basic_prd.py     <- current: dumb baseline
├── agents/                <- each agent gets its own file, built one at a time
├── outputs/                <- generated PRDs land here
├── requirements.txt
└── .env.example
```
