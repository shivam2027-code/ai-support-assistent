from langchain_huggingface import HuggingFaceEndpointEmbeddings

from app.core.config import settings


embeddings = HuggingFaceEndpointEmbeddings(
    model="BAAI/bge-small-en-v1.5",
    huggingfacehub_api_token=settings.HUGGINGFACE_API_KEY
)


def create_embeddings(chunks: list[dict]):

    texts = [chunk["text"] for chunk in chunks]

    vectors = embeddings.embed_documents(texts)

    return vectors