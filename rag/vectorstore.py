import os

from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient

load_dotenv()


AZURE_SEARCH_ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT")
AZURE_SEARCH_API_KEY = os.getenv("AZURE_SEARCH_API_KEY")

INDEX_NAME = "production-agent-index"


if not AZURE_SEARCH_ENDPOINT:
    raise ValueError("AZURE_SEARCH_ENDPOINT is not set")

if not AZURE_SEARCH_API_KEY:
    raise ValueError("AZURE_SEARCH_API_KEY is not set")


search_client = SearchClient(
    endpoint=AZURE_SEARCH_ENDPOINT,
    index_name=INDEX_NAME,
    credential=AzureKeyCredential(AZURE_SEARCH_API_KEY),
)


def upload_documents(documents: list[dict]) -> None:
    """
    Upload chunked documents with embeddings to Azure AI Search.
    """

    if not documents:
        return

    result = search_client.upload_documents(documents=documents)

    failed = [
        item
        for item in result
        if not item.succeeded
    ]

    if failed:
        raise RuntimeError(
            f"Failed to upload {len(failed)} documents"
        )

    print(f"Uploaded {len(documents)} documents successfully")
