import os

from dotenv import load_dotenv
from langchain_ollama import OllamaEmbeddings

load_dotenv()


OLLAMA_URL = os.getenv("OLLAMA_URL")
EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "nomic-embed-text",
)


embeddings = OllamaEmbeddings(
    model=EMBEDDING_MODEL,
    base_url=OLLAMA_URL,
)


def generate_embeddings(texts: list[str]) -> list[list[float]]:
    """
    Generate embeddings for a list of texts.
    """

    if not texts:
        return []

    return embeddings.embed_documents(texts)
