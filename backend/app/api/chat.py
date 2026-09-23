
from fastapi import APIRouter

from app.schemas.chat import ChatRequest, ChatResponse
from app.services.rag_service import generate_answer


router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


@router.post(
    "/",
    response_model=ChatResponse
)
def chat(request: ChatRequest):

    result = generate_answer(
        question=request.question,
        session_id=request.session_id
    )

    return result

