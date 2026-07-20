# use the TavilySearch tool to perform a search query with a maximum of 5 results

from langchain_tavily import TavilySearch

from app.config import TAVILY_API_KEY   
from langchain_text_splitters  import RecursiveCharacterTextSplitter  
from langchain_core.documents import Document

search_tool = TavilySearch(
    max_results=5,
    tavily_api_key=TAVILY_API_KEY
)
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=150,
)

def travily_to_documents(search_response : dict):
    """
    Convert the Tavily search response to a list of Document objects.
    
    Args:
        search_response (dict): The response from the Tavily search API.
        
    Returns:
        List[Document]: A list of Document objects containing the page content and metadata.
    """
    documents = []
    for item in search_response["results"]:
        
        text = item.get("raw_content") or item.get("content" , "")
        
        document =Document(
                page_content=text,
                metadata={
                    "title": item.get("title"),
                    "url": item.get("url"),
                    "score": item.get("score"),
                }
            )
        chunks = text_splitter.split_documents([document])
        documents.extend(chunks)
        
    return documents
        