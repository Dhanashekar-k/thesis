import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch

load_dotenv()

tools = [
    TavilySearch(max_results=5),
]

VLLM_BASE_URL = os.getenv("VLLM_BASE_URL", "http://127.0.0.1:8000/v1")
VLLM_MODEL = os.getenv("VLLM_MODEL", "Qwen/Qwen2.5-VL-72B-Instruct")
VLLM_API_KEY = os.getenv("VLLM_API_KEY", "EMPTY")

llm = ChatOpenAI(
    model=VLLM_MODEL,
    base_url=VLLM_BASE_URL,
    api_key=VLLM_API_KEY,
    temperature=0.7,
    timeout=120,
    max_retries=2,
).bind_tools(tools)