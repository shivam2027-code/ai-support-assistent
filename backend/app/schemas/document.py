from pydantic import BaseModel


class DocumentResponse(BaseModel):

    filename: str
    pages: int
    chunks: int
    embedding_dimension: int
    session_id: str