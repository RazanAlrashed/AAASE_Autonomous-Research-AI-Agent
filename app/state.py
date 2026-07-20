from typing import TypedDict

class ResearchState(TypedDict):
    query : str
    search_results: list
    documents : list
    retrieved_documents: list
    analysis : str
    quality_score : int
    quality_reason : str
    iteration_count :int
    report : str
    audit_log : list
    sources : list[str]
    