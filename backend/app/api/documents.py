import tempfile
import uuid

from fastapi import APIRouter, UploadFile, File, HTTPException

from app.services.document_service import process_pdf
from app.schemas.document import DocumentResponse


router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)


@router.post(
    "/upload",
    response_model=DocumentResponse
)
async def upload_document(
    file: UploadFile = File(...)
):

    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )

    # Create unique session ID
    session_id = str(uuid.uuid4())

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf"
    ) as temp_file:

        content = await file.read()

        temp_file.write(content)

        temp_file_path = temp_file.name

    result = process_pdf(
        temp_file_path,
        file.filename,
        session_id
    )

    return {
        "filename": file.filename,
        "pages": result["pages"],
        "chunks": len(result["chunks"]),
        "embedding_dimension": 384,
        "session_id": session_id
    }