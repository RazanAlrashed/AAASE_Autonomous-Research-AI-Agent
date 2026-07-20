from app.search import search_tool , travily_to_documents
from app.state import ResearchState
from app.vector_store import vector_db , retrieve
from app.llm import llm
from app.prompt import analysis_prompt , quality_prompt , report_prompt , refine_prompt
from app.models import QualityScore
from datetime import datetime
import json
from app.utils import retry

def research_collection (state: ResearchState):
    
    print("Searching the web ....")
    
    results = search_tool.invoke(state["query"])
    
    return {
        "search_results": results
    }
   

def memory_storge(
    state: ResearchState,
):
    """
    Store the retrieved documents in the vector database.
    
    Args:
        state (ResearchState): The current state of the research process.
    """
    print("storing document...")
    
    docs = travily_to_documents(state["search_results"])
    print(f"Chunks created: {len(docs)}")
    
    for d in docs[:3]:
        print("="*60)
        print(d.page_content[:200])
        print(d.metadata)
        
    vector_db.reset_collection()


    vector_db.add_documents(docs)
    
    return {
        "documents": docs
    }
    
    
def analysis(state):
    print("Analyzing the research ...")
    
    retrived_docs = retrieve(state["query"], k=5)
    print("Retrieved:", len(retrived_docs))
    for doc in retrived_docs:
        print(doc.metadata)
        
    if not retrived_docs:

        return {
            "analysis": "No relevant documents were found.",
            "retrieved_documents": [],
            "sources": [],
        }
    # convert the retrieved documents to a single string for analysis since llm can only take a single string as input

    context = "\n\n".join(

    f"""
    ==================================================
    DOCUMENT {i+1}
    
    Title:
    {doc.metadata.get("title")}

    Source:
    {doc.metadata.get("url")}

    Content:
    {doc.page_content[:1200]}
    """

        for i , doc in enumerate(retrived_docs)
    )
        
    prompt = analysis_prompt.invoke(
        {
        "query" : state["query"], 
        "documents" : context
        }
    )
    
    response = retry(lambda: llm.invoke(prompt))
    
    return {
        "retrieved_documents": retrived_docs,
        "analysis": response.content,
        "sources" : [
            doc.metadata.get("url") 
            for doc in retrived_docs
            ]
    }

def quality_evaluation(state):

    print("Evaluating research quality...")

    prompt = quality_prompt.invoke(
        {
            "query": state["query"],
            "analysis": state["analysis"],
            "sources": "\n".join(state["sources"]),

        }
    )

    response = retry(
        lambda: llm.invoke(prompt)
    )
    data = json.loads(response.content)

    result = QualityScore(**data)

    return {
        "quality_score": result.score,
        "quality_reason": result.reasoning,
    }
    
    
def report_generation(state):

    print("Generating final report...")

    prompt = report_prompt.invoke(
        {
            "query": state["query"],
            "analysis": state["analysis"],
            "sources": "\n".join(state["sources"])

        }
    )
    
    response = retry(
    lambda: llm.invoke(prompt)
)


    return {
        "report": response.content
    }
    

def audit(state):

    print("Writing audit log...")

    log = {
        "timestamp": datetime.now().isoformat(),

        "query": state["query"],

        "quality_score": state["quality_score"],

        "iterations": state["iteration_count"],
    }

    logs = state.get("audit_log", [])

    logs.append(log)

    return {
        "audit_log": logs
    }
    
    
def refine_query(state):

    print("Refining query...")

    prompt = refine_prompt.invoke(
        {
            "query": state["query"],
            "reason": state["quality_reason"],
        }
    )

    response = retry(
        lambda: llm.invoke(prompt)
    )
    new_query = response.content.strip()

    # Remove markdown

    new_query = new_query.replace("```", "")

    # Remove quotes

    new_query = new_query.replace('"', "")

    # Remove labels

    new_query = new_query.replace(
        "Here is the improved query:",
        ""
    )

    new_query = new_query.strip()

    # Tavily limit

    new_query = new_query[:150]

    return {

        "query": new_query,

        "iteration_count":
            state["iteration_count"] + 1
    }
MAX_RESEARCH_ITERATIONS = 3


def route_after_quality(state):

    score = state["quality_score"]

    iterations = state["iteration_count"]

    if score >= 7:

        return "report_generation"

    if iterations >= MAX_RESEARCH_ITERATIONS:

        print("Maximum iterations reached.")

        return "report_generation"

    return "refine_query"