from langchain_text_splitters import RecursiveCharacterTextSplitter


# --------------------------------------------------
# Chunk configuration
# --------------------------------------------------

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200


splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP,
    separators=[
        "\n\n",
        "\n",
        ". ",
        " ",
        "",
    ],
)


def chunk_documents(documents: list[dict]) -> list[dict]:
    """
    Split page-level documents into smaller chunks.
    """

    chunks = []

    for document in documents:

        content = document["content"]

        page_number = document["pageNumber"]
        source = document["source"]

        split_texts = splitter.split_text(content)

        for chunk_index, chunk_text in enumerate(split_texts):

            chunk_text = chunk_text.strip()

            if not chunk_text:
                continue

            chunks.append(
                {
                    "content": chunk_text,
                    "pageNumber": page_number,
                    "source": source,
                    "chunkId": f"{source.replace('.pdf', '')}-{page_number}-{chunk_index}",
                }
            )

    return chunks
