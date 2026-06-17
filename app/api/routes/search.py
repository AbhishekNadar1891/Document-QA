import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.schemas import SearchRequest
from app.database.session import get_db
from app.services.embedding_service import EmbeddingService
from app.services.retrieval_service import RetrievalService
from app.services.vector_store import VectorStore

router = APIRouter()
logger = logging.getLogger(__name__)

vector_store = VectorStore()
embedder = EmbeddingService()
retriever = RetrievalService()

@router.post("")
def search(request: SearchRequest, db: Session = Depends(get_db)):
    query_embedding = embedder.embed_query(request.query)
    retrieval = retriever.retrieve(request.query, query_embedding)
    results = [
        {
            "document_id": item["document_id"],
            "filename": item["filename"],
            "chunk_id": item["chunk_id"],
            "page_number": item["page_number"],
            "text": item["text"],
            "similarity": item["similarity"],
        }
        for item in retrieval["sources"]
    ]
    logger.info("Semantic search performed for query: %s", request.query)
    return {"results": results}
