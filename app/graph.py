from langgraph.graph import StateGraph, START, END
from app.state import ResearchState

from app.node import(
    research_collection,
    memory_storge,
    analysis,
    quality_evaluation,
    report_generation,
    audit,
    refine_query,
    route_after_quality
    
)


builder = StateGraph(ResearchState)


builder.add_node(
    "research_collection",
    research_collection,
)

builder.add_node(
    "memory_storge",
    memory_storge,
)

builder.add_node(               
    "analysis",
    analysis,
)

builder.add_node(
    "quality_evaluation",
    quality_evaluation, 
)
builder.add_node(
    "report_generation",
    report_generation,
)
builder.add_node(
    "audit",
    audit,
)
builder.add_node(
    "refine_query",
    refine_query,
)


builder.add_edge(START, "research_collection")
builder.add_edge("research_collection", "memory_storge")
builder.add_edge("memory_storge", "analysis")
builder.add_edge("analysis", "quality_evaluation")
builder.add_conditional_edges(
    "quality_evaluation",route_after_quality)
builder.add_edge("report_generation", "audit")
builder.add_edge("audit", END)
builder.add_edge("refine_query", "research_collection")

graph = builder.compile()
