# Configuration file for the application

from dotenv import load_dotenv
import os

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL")
LLM_MODEL = os.getenv("LLM_MODEL")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")