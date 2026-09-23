from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PayloadSchemaType
)

from app.core.config import settings
from app.rag.embeddings import embeddings


COLLECTION_NAME = "ai_support_documents"


# Connect to Qdrant Cloud
client = QdrantClient(
    url=settings.QDRANT_URL,
    api_key=settings.QDRANT_API_KEY
)


def create_collection():

    collections = client.get_collections()

    collection_names = [
        collection.name
        for collection in collections.collections
    ]

    # Create collection if it doesn't exist
    if COLLECTION_NAME not in collection_names:

        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=384,
                distance=Distance.COSINE
            )
        )

        print(f"Created collection: {COLLECTION_NAME}")

    else:

        print(f"Collection already exists: {COLLECTION_NAME}")


def create_session_index():

    client.create_payload_index(
        collection_name=COLLECTION_NAME,
        field_name="metadata.session_id",
        field_schema=PayloadSchemaType.KEYWORD
    )

    print("Session ID payload index created")


# Create collection first
create_collection()

# Create index for session-based filtering
create_session_index()


# Create LangChain Qdrant vector store
vector_store = QdrantVectorStore(
    client=client,
    collection_name=COLLECTION_NAME,
    embedding=embeddings
)