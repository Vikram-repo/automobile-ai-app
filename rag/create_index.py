import os

from dotenv import load_dotenv

from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex,
    SearchField,
    SearchFieldDataType,
    SimpleField,
    SearchableField,
    VectorSearch,
    HnswAlgorithmConfiguration,
    VectorSearchProfile,
)

load_dotenv()


# --------------------------------------------------
# Configuration
# --------------------------------------------------

AZURE_SEARCH_ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT")
AZURE_SEARCH_API_KEY = os.getenv("AZURE_SEARCH_API_KEY")

INDEX_NAME = "production-agent-index"


# --------------------------------------------------
# Validation
# --------------------------------------------------

if not AZURE_SEARCH_ENDPOINT:
    raise ValueError("AZURE_SEARCH_ENDPOINT is not set")

if not AZURE_SEARCH_API_KEY:
    raise ValueError("AZURE_SEARCH_API_KEY is not set")


# --------------------------------------------------
# Search Client
# --------------------------------------------------

index_client = SearchIndexClient(
    endpoint=AZURE_SEARCH_ENDPOINT,
    credential=AzureKeyCredential(AZURE_SEARCH_API_KEY),
)


# --------------------------------------------------
# Vector Search Configuration
# --------------------------------------------------

vector_search = VectorSearch(
    algorithms=[
        HnswAlgorithmConfiguration(
            name="hnsw-config",
        )
    ],
    profiles=[
        VectorSearchProfile(
            name="hnsw-profile",
            algorithm_configuration_name="hnsw-config",
        )
    ],
)


# --------------------------------------------------
# Index Fields
# --------------------------------------------------

fields = [

    # Primary key
    SimpleField(
        name="id",
        type=SearchFieldDataType.String,
        key=True,
        filterable=True,
    ),

    # Actual chunk text
    SearchableField(
        name="content",
        type=SearchFieldDataType.String,
        searchable=True,
        retrievable=True,
    ),

    # 768-dimensional embedding
    SearchField(
        name="contentVector",
        type=SearchFieldDataType.Collection(
            SearchFieldDataType.Single
        ),
        searchable=True,
        vector_search_dimensions=768,
        vector_search_profile_name="hnsw-profile",
    ),

    # Metadata
    SimpleField(
        name="documentId",
        type=SearchFieldDataType.String,
        filterable=True,
        retrievable=True,
    ),

    SearchableField(
        name="documentName",
        type=SearchFieldDataType.String,
        searchable=True,
        filterable=True,
        retrievable=True,
    ),

    SimpleField(
        name="chunkId",
        type=SearchFieldDataType.String,
        filterable=True,
        retrievable=True,
    ),

    SimpleField(
        name="pageNumber",
        type=SearchFieldDataType.Int32,
        filterable=True,
        sortable=True,
        retrievable=True,
    ),

    SearchableField(
        name="source",
        type=SearchFieldDataType.String,
        searchable=True,
        filterable=True,
        retrievable=True,
    ),

    # Important for future RBAC filtering
    SearchableField(
        name="department",
        type=SearchFieldDataType.String,
        searchable=True,
        filterable=True,
        retrievable=True,
    ),
]


# --------------------------------------------------
# Create Index
# --------------------------------------------------

index = SearchIndex(
    name=INDEX_NAME,
    fields=fields,
    vector_search=vector_search,
)


result = index_client.create_or_update_index(index)

print(f"Index created successfully: {result.name}")
