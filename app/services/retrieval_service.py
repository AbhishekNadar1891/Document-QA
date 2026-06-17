import logging
from typing import List
from app.services.vector_store import VectorStore
from app.config.settings import settings

logger = logging.getLogger(__name__)

class RetrievalService:
    def __init__(self):
        self.vector_store = VectorStore()

    def retrieve(self, query: str, query_embedding: List[float]) -> dict:
        raw_results = self.vector_store.search(query_embedding, top_k=settings.TOP_K)
        filtered = [item for item in raw_results if item["similarity"] >= settings.MIN_SIMILARITY]
        sources = []
        chunks = []
        for item in filtered:
            sources.append(item)
            chunks.append({
                "document_id": item["document_id"],
                "chunk_id": item["chunk_id"],
                "page_number": item["page_number"],
                "text": item["text"],
                "similarity": item["similarity"],
            })
        logger.info("Retrieved %s chunks for query", len(chunks))
        return {"chunks": chunks, "sources": sources}
