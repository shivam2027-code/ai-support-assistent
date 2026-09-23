from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.documents import router as documents_router
from app.api.chat import router as chat_router

app = FastAPI(
    title="AI Support Agent",
    description="RAG-based AI customer support API",
    version="1.0.0"
)

# Allow React frontend to communicate with FastAPI

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://ai-support-assistent-71xhihgzk-team-hydra3.vercel.app/"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)













app.include_router(documents_router)
app.include_router(chat_router)


@app.get("/")
def root():
    return {
        "message": "AI Support Agent API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }