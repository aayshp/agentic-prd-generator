
import streamlit as st
from graph import run_pipeline
from pdf_export import markdown_to_pdf_bytes

st.set_page_config(page_title="Agentic PRD Generator", page_icon="🧩", layout="wide")

st.title("🧩 Agentic PRD Generator")
st.caption(
    "Not a single AI prompt. A pipeline of 5 agents — Requirement Gathering, "
    "Persona, Feature Prioritization, PRD Writer, and a Reviewer that sends "
    "work back for revision until it's actually good enough."
)

idea = st.text_area(
    "Describe your product idea:",
    placeholder="e.g. A predictive temperature alert system for a pharma "
                "manufacturing line, to reduce batch failures before they happen.",
    height=100,
)

if st.button("Run the agent pipeline", type="primary", disabled=not idea):
    with st.spinner("Running agents... this takes 30-60 seconds"):
        result = run_pipeline(idea)

    st.success(
        f"Done — approved after {result['revision_count']} review round"
        f"{'s' if result['revision_count'] != 1 else ''}"
    )

    tab1, tab2 = st.tabs(["📄 Final PRD", "🔍 Agent-by-agent trace"])

    with tab1:
        st.markdown(result["prd_draft"])

        col1, col2 = st.columns(2)
        with col1:
            pdf_bytes = markdown_to_pdf_bytes(result["prd_draft"])
            st.download_button(
                "📄 Download as PDF",
                pdf_bytes,
                file_name="prd_output.pdf",
                mime="application/pdf",
            )
        with col2:
            st.download_button(
                "Download as Markdown (for developers)",
                result["prd_draft"],
                file_name="prd_output.md",
            )

    with tab2:
        st.write("This is what each agent actually did, in order:")
        for i, step in enumerate(result["agent_trace"], 1):
            with st.expander(f"{i}. {step['agent']}"):
                st.json(step["output"]) if isinstance(step["output"], dict) else st.write(step["output"])
