📚 Enterprise Autonomous Research Agent

An autonomous research agent built with LangGraph that searches the web, stores results in a vector database, analyzes them with an LLM, evaluates its own output quality, and iteratively refines its search query until it produces a reliable, source-grounded report — complete with an audit trail.

A Streamlit interface is included so you can run research topics through the pipeline and watch it work in real time.

✨ Features
🔎 Web search via Tavily, chunked and embedded into a vector store
🧠 Grounded analysis — the LLM is instructed to answer only from retrieved documents, never its own knowledge
✅ Self-evaluation loop — a quality score (1–10) decides whether to generate the final report or refine the query and search again
🔁 Automatic query refinement with a max iteration cap to prevent infinite loops
📝 Structured enterprise report (Executive Summary, Key Findings, Opportunities, Risks, Recommendations, Conclusion, References)
📋 Audit log of every research run (timestamp, query, quality score, iteration count)
🖥️ Streamlit UI with live progress tracking, quality score display, and a downloadable Markdown report
🏗️ Architecture

The pipeline is a LangGraph state machine:

START
  → research_collection      (Tavily web search)
  → memory_storge            (chunk + embed into Chroma)
  → analysis                 (retrieve relevant chunks, LLM analysis)
  → quality_evaluation       (LLM scores the analysis 1–10)
      ├── score ≥ 7 or max iterations reached → report_generation → audit → END
      └── score < 7                            → refine_query → research_collection (loop)

You can find the final report in (final_report.md)
      
<img width="1917" height="1021" alt="Screenshot 2026-07-20 215613" src="https://github.com/user-attachments/assets/a11eb2b8-e812-4775-86f9-7ef64f49bcd9" />


<img width="1905" height="1021" alt="Screenshot 2026-07-20 215924" src="https://github.com/user-attachments/assets/a094f7f7-8af4-461b-85d2-c39c7d29b2b5" />



