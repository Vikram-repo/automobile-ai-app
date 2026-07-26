import os
from dotenv import load_dotenv
from langchain_ollama import ChatOllama

load_dotenv()

llm = ChatOllama(
    model=os.getenv("MODEL_NAME"),
    base_url=os.getenv("OLLAMA_URL"),
)