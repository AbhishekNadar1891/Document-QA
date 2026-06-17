from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter
from slowapi.middleware import SlowAPIMiddleware
from app.config.settings import settings
from app.api.routes.documents import router as documents_router
from app.api.routes.chat import router as chat_router
from app.api.routes.search import router as search_router
from app.database.session import engine, Base
from app.utils.logger import configure_logging
import os

configure_logging()

app = FastAPI(
    title="RAG Platform",
    description="Enterprise-ready Retrieval-Augmented Generation platform.",
    version="0.1.0",
)

limiter = Limiter(key_func=lambda request: request.client.host, default_limits=[settings.RATE_LIMIT])
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(documents_router, prefix="/documents", tags=["documents"])
app.include_router(chat_router, prefix="/chat", tags=["chat"])
app.include_router(search_router, prefix="/search", tags=["search"])

@app.on_event("startup")
def startup_event():
    os.makedirs(settings.DATA_DIR, exist_ok=True)
    os.makedirs(settings.VECTOR_DIR, exist_ok=True)
    os.makedirs(os.path.dirname(settings.LOG_FILE), exist_ok=True)
    Base.metadata.create_all(bind=engine)

@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok"}
