from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizedQuery

from rag.config import (
    AZURE_SEARCH_ENDPOINT,
    AZURE_SEARCH_API_KEY,
    AZURE_SEARCH_INDEX,
)
from rag.embeddings import generate_embeddings


search_client = SearchClient(
    endpoint=AZURE_SEARCH_ENDPOINT,
    index_name=AZURE_SEARCH_INDEX,
    credential=AzureKeyCredential(AZURE_SEARCH_API_KEY),
)


def retrieve_documents(
    query: str,
    top_k: int = 5,
) -> list[dict]:
    """
    Retrieve relevant documents from Azure AI Search
    using vector similarity.
    """

    query_vector = generate_embeddings([query])[0]

    vector_query = VectorizedQuery(
        vector=query_vector,
        k_nearest_neighbors=top_k,
        fields="contentVector",
    )

    results = search_client.search(
        search_text=None,
        vector_queries=[vector_query],
        select=[
            "id",
            "content",
            "documentId",
            "documentName",
            "chunkId",
            "pageNumber",
            "source",
            "department",
        ],
        top=top_k,
    )

    documents = []

    for result in results:
        documents.append(
            {
                "content": result["content"],
                "documentName": result.get("documentName"),
                "pageNumber": result.get("pageNumber"),
                "source": result.get("source"),
                "score": result.get("@search.score"),
            }
        )

    return documents
