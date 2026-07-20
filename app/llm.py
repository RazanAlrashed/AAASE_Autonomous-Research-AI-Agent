# This file is used to initialize the LLM model using the OpenRouter API. It imports the necessary configuration variables from the config.py file and creates an instance of the ChatOpenAI class with the specified model, API key, base URL, and temperature.
from langchain_openai import ChatOpenAI

from app.config import (
    OPENROUTER_API_KEY,
    OPENROUTER_BASE_URL,    
    LLM_MODEL
)


llm = ChatOpenAI(
    model=LLM_MODEL,
    api_key=OPENROUTER_API_KEY,
    base_url=OPENROUTER_BASE_URL,
    temperature=0
)