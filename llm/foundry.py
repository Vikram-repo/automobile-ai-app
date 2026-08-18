import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from tools import tools

load_dotenv()

foundry_llm = ChatOpenAI(
    model=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    base_url=os.getenv("AZURE_OPENAI_ENDPOINT") + "/openai/v1/",
    temperature=0,
)

foundry_llm_with_tools = foundry_llm.bind_tools(tools)
