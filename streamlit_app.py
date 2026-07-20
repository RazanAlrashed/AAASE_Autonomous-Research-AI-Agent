# Streamlit interface for the Enterprise Autonomous Research Agent.
#
# This file lives OUTSIDE the `app/` package, at the same level as main.py,
# so it can simply do `from app.graph import graph`.
#
# Run with:
#   pip install streamlit
#   streamlit run streamlit_app.py

import streamlit as st

from app.graph import graph

st.set_page_config(
    page_title="Enterprise Autonomous Research Agent",
    page_icon="📚",
    layout="centered",
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

# Friendly labels for each graph node, in the order the pipeline usually runs.
STEP_LABELS = {
    "research_collection": "Searching...",
    "memory_storge": "Storing...",
    "analysis": "Analysis...",
    "quality_evaluation": "Quality...",
    "refine_query": "Refining query...",
    "report_generation": "Generating...",
    "audit": "Logging audit...",
}

PIPELINE_ORDER = [
    "research_collection",
    "memory_storge",
    "analysis",
    "quality_evaluation",
    "report_generation",
    "audit",
]


def render_progress(progress_slot, completed: list[str], active: str | None):
    """Render a simple checklist of pipeline steps with the current one highlighted."""
    lines = []
    seen_refine = completed.count("refine_query")

    for node_name in PIPELINE_ORDER:
        label = STEP_LABELS[node_name]
        if node_name in completed:
            lines.append(f"✅ {label}")
        elif node_name == active:
            lines.append(f"🔄 {label}")
        else:
            lines.append(f"⬜ {label}")

    if seen_refine:
        lines.append(f"↩️ Refined query {seen_refine}x and re-ran search")

    progress_slot.markdown("\n\n".join(lines))


# ---------------------------------------------------------------------------
# UI
# ---------------------------------------------------------------------------

st.title("📚 Enterprise Autonomous Research Agent")

with st.form("research_form"):
    query = st.text_input(
        "Research Topic",
        placeholder="Latest AI applications in education",
    )
    submitted = st.form_submit_button("Start Research", type="primary", use_container_width=True)

if submitted:
    if not query.strip():
        st.warning("Please enter a research topic.")
    else:
        st.divider()

        st.subheader("Progress")
        progress_slot = st.empty()

        score_slot = st.container()
        report_slot = st.container()

        completed_steps: list[str] = []
        final_score = None
        final_reason = None
        final_report = None

        render_progress(progress_slot, completed_steps, active="research_collection")

        initial_state = {
            "query": query,
            "iteration_count": 0,
            "audit_log": [],
        }

        try:
            for step in graph.stream(initial_state, stream_mode="updates"):
                for node_name, output in step.items():
                    completed_steps.append(node_name)

                    # Figure out what's "next" for the active indicator.
                    if node_name == "refine_query":
                        active_next = "research_collection"
                    elif node_name in PIPELINE_ORDER:
                        idx = PIPELINE_ORDER.index(node_name)
                        active_next = PIPELINE_ORDER[idx + 1] if idx + 1 < len(PIPELINE_ORDER) else None
                    else:
                        active_next = None

                    render_progress(progress_slot, completed_steps, active=active_next)

                    if node_name == "quality_evaluation":
                        final_score = output.get("quality_score")
                        final_reason = output.get("quality_reason")

                    if node_name == "report_generation":
                        final_report = output.get("report")

            render_progress(progress_slot, completed_steps, active=None)

        except Exception as e:
            st.error(f"An error occurred while running the pipeline: {e}")

        # ---- Quality score ----
        if final_score is not None:
            with score_slot:
                st.divider()
                st.subheader("Quality Score")
                st.metric(label="", value=f"{final_score}/10")
                if final_reason:
                    with st.expander("Why this score?"):
                        st.write(final_reason)

        # ---- Final report ----
        if final_report:
            with report_slot:
                st.divider()
                st.subheader("Report")
                st.markdown(final_report)

                st.download_button(
                    "Download report (.md)",
                    data=final_report,
                    file_name="research_report.md",
                    mime="text/markdown",
                )