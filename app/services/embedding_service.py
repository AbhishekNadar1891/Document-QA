import logging
from pathlib import Path
from typing import List
from sentence_transformers import SentenceTransformer
import numpy as np
from app.config.settings import settings

logger = logging.getLogger(__name__)

class EmbeddingService:
    _model: SentenceTransformer | None = None

    def __init__(self):
        if EmbeddingService._model is None:
            self._load_model()

    def _load_model(self):
        temp_model = SentenceTransformer(settings.EMBEDDING_MODEL)
        device = temp_model.device.type if hasattr(temp_model, "device") else "cpu"
        logger.info("Loading embedding model on %s", device)
        EmbeddingService._model = SentenceTransformer(settings.EMBEDDING_MODEL, device=device)

    @property
    def model(self) -> SentenceTransformer:
        if EmbeddingService._model is None:
            self._load_model()
        return EmbeddingService._model

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        embeddings = self.model.encode(texts, batch_size=16, convert_to_numpy=True, normalize_embeddings=True)
        return embeddings.tolist()

    def embed_query(self, query: str) -> List[float]:
        embedding = self.model.encode([query], convert_to_numpy=True, normalize_embeddings=True)
        return embedding[0].tolist()

    def normalize_embeddings(self, embeddings: List[List[float]]) -> List[List[float]]:
        array = np.array(embeddings, dtype=np.float32)
        norms = np.linalg.norm(array, axis=1, keepdims=True)
        return (array / np.maximum(norms, 1e-9)).tolist()
