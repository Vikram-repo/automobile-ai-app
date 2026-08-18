import os

from dotenv import load_dotenv
from langchain_ollama import ChatOllama

from tools import tools
from prompts.system_prompt import SYSTEM_PROMPT

load_dotenv()

llm = ChatOllama(
    model=os.getenv("MODEL_NAME"),
    base_url=os.getenv("OLLAMA_URL"),
    timeout=20,
    temperature=0,
)

llm_with_tools = llm.bind_tools(tools)
