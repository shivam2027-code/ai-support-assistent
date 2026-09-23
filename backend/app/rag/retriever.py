
from app.rag.vector_store import vector_store


def retrieve_documents(
    question: str,
    session_id: str,
    k: int = 5
):

    documents = vector_store.similarity_search_with_score(
        query=question,
        k=k,
        filter={
            "must": [
                {
                    "key": "metadata.session_id",
                    "match": {
                        "value": session_id
                    }
                }
            ]
        }
    )

    return documents

