import os

from dotenv import load_dotenv

load_dotenv()


AZURE_SEARCH_ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT")
AZURE_SEARCH_API_KEY = os.getenv("AZURE_SEARCH_API_KEY")
AZURE_SEARCH_INDEX = os.getenv(
    "AZURE_SEARCH_INDEX",
    "production-agent-index",
)
