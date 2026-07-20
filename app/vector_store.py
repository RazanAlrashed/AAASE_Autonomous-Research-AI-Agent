from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

EMBEDDINGS_MODEL = "BAAI/bge-small-en-v1.5"

embeddings = HuggingFaceEmbeddings(model_name=EMBEDDINGS_MODEL)

vector_db = Chroma(
    collection_name="research_memory",
    embedding_function=embeddings,
    persist_directory="./chroma_db"
)

def retrieve (query: str, k: int = 3):
    return vector_db.similarity_search(query, k=3)
  