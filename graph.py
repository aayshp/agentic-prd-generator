"""
THE ORCHESTRATOR - wires every agent into one graph with a real LOOP
(Reviewer -> back to PRD Writer -> Reviewer again, until approved or
safety limit hit). This is the file that proves it's a system, not a
single prompt.
"""
from langgraph.graph import StateGraph, END
from state import PRDState
import requirement_agent
import persona_agent
import prioritization_agent
import prd_writer_agent
import reviewer_agent


def build_graph():
    graph = StateGraph(PRDState)

    graph.add_node("requirements", requirement_agent.run)
    graph.add_node("persona", persona_agent.run)
    graph.add_node("prioritization", prioritization_agent.run)
    graph.add_node("prd_writer", prd_writer_agent.run)
    graph.add_node("reviewer", reviewer_agent.run)

    graph.set_entry_point("requirements")
    graph.add_edge("requirements", "persona")
    graph.add_edge("persona", "prioritization")
    graph.add_edge("prioritization", "prd_writer")
    graph.add_edge("prd_writer", "reviewer")

    graph.add_conditional_edges(
        "reviewer",
        reviewer_agent.should_revise,
        {"revise": "prd_writer", "end": END}
    )

    return graph.compile()


def run_pipeline(idea: str):
    app = build_graph()
    initial_state: PRDState = {
        "idea": idea,
        "requirements": {},
        "persona": {},
        "prioritization": {},
        "prd_draft": "",
        "review_feedback": None,
        "revision_count": 0,
        "is_approved": False,
        "agent_trace": [],
    }
    return app.invoke(initial_state)
