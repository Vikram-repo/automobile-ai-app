import os

from dotenv import load_dotenv
from tavily import TavilyClient

from langchain_core.tools import tool

load_dotenv()

client = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)


@tool
def internet_search(query: str) -> str:
    """
    Search the internet for recent information.
    """

    response = client.search(
        query=query,
        max_results=5,
    )

    return str(response["results"])