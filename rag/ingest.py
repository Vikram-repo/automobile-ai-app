from pathlib import Path

from rag.loader import load_pdf
from rag.chunker import chunk_documents
from rag.embeddings import generate_embeddings
from rag.vectorstore import upload_documents


DOCUMENTS_DIR = Path("documents")


def ingest_pdf(file_path: str, department: str = "general"):
    print(f"Loading: {file_path}")

    # 1. Load PDF page by page
    pages = load_pdf(file_path)

    print(f"Pages loaded: {len(pages)}")

    # 2. Create chunks
    chunks = chunk_documents(pages)

    print(f"Chunks created: {len(chunks)}")

    if not chunks:
        print("No chunks found.")
        return

    # 3. Generate embeddings
    texts = [chunk["content"] for chunk in chunks]

    vectors = generate_embeddings(texts)

    print(f"Embeddings generated: {len(vectors)}")

    # 4. Prepare Azure AI Search documents
    documents = []

    file_name = Path(file_path).name
    document_id = Path(file_path).stem

    for chunk, vector in zip(chunks, vectors):

        documents.append(
            {
                "id": chunk["chunkId"],
                "content": chunk["content"],
                "contentVector": vector,
                "documentId": document_id,
                "documentName": file_name,
                "chunkId": chunk["chunkId"],
                "pageNumber": chunk["pageNumber"],
                "source": chunk["source"],
                "department": department,
            }
        )

    # 5. Upload to Azure AI Search
    upload_documents(documents)

    print("Ingestion completed successfully.")


if __name__ == "__main__":

    pdf_files = list(DOCUMENTS_DIR.glob("*.pdf"))

    if not pdf_files:
        raise FileNotFoundError(
            "No PDF files found inside documents/"
        )

    for pdf_file in pdf_files:
        ingest_pdf(
            str(pdf_file),
            department="general",
        )
