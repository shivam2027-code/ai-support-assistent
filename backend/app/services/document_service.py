import os

from app.rag.loader import load_pdf
from app.rag.splitter import split_pages
from app.rag.vector_store import vector_store


def process_pdf(
    file_path: str,
    filename: str,
    session_id: str
):

    pages = load_pdf(file_path)

    chunks = split_pages(pages)

    texts = [
        chunk["text"]
        for chunk in chunks
    ]

    metadatas = [
        {
            "page": chunk["page"],
            "filename": filename,
            "session_id": session_id
        }
        for chunk in chunks
    ]

    vector_store.add_texts(
        texts=texts,
        metadatas=metadatas
    )

    os.remove(file_path)

    return {
        "pages": len(pages),
        "chunks": chunks
    }