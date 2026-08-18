from langchain_core.tools import tool

from rag.retriever import retrieve_documents


@tool
def search_knowledge_base(query: str) -> str:
    """
    Search the internal knowledge base for relevant information.
    """

    documents = retrieve_documents(
        query=query,
        top_k=5,
    )

    if not documents:
        return "No relevant information found in the knowledge base."

    results = []

    for doc in documents:
        results.append(
            f"""
Source: {doc["source"]}
Page: {doc["pageNumber"]}

Content:
{doc["content"]}
"""
        )

    return "\n---\n".join(results)
