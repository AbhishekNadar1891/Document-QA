import json
import os
from pathlib import Path
from typing import List
import faiss
import numpy as np
from app.config.settings import settings

class VectorStore:
    def __init__(self):
        self.index_path = settings.VECTOR_INDEX_FILE
        self.metadata_path = settings.VECTOR_METADATA_FILE
        self.dimension = 384
        self.index = None
        self.metadata = []
        self._load_index()

    def _create_index(self):
        self.index = faiss.IndexFlatIP(self.dimension)

    def _load_index(self):
        if self.index_path.exists() and self.metadata_path.exists():
            self.index = faiss.read_index(str(self.index_path))
            with open(self.metadata_path, "r", encoding="utf-8") as f:
                self.metadata = json.load(f)
        else:
            self._create_index()
            self.save_index()

    def save_index(self):
        os.makedirs(self.index_path.parent, exist_ok=True)
        faiss.write_index(self.index, str(self.index_path))
        with open(self.metadata_path, "w", encoding="utf-8") as f:
            json.dump(self.metadata, f, ensure_ascii=False, indent=2)

    def add_vectors(self, chunks: List[dict], embeddings: List[List[float]]):
        array = np.array(embeddings, dtype=np.float32)
        self.index.add(array)
        for chunk, embedding in zip(chunks, embeddings):
            self.metadata.append({
                "document_id": chunk["document_id"],
                "chunk_id": chunk["chunk_id"],
                "page_number": chunk["page_number"],
                "text": chunk["text"],
            })
        self.save_index()

    def search(self, query_embedding: List[float], top_k: int = 5):
        if self.index is None or self.index.ntotal == 0:
            return []
        array = np.array([query_embedding], dtype=np.float32)
        scores, indices = self.index.search(array, top_k)
        results = []
        for score, index in zip(scores[0], indices[0]):
            if index < 0 or index >= len(self.metadata):
                continue
            item = self.metadata[index].copy()
            item["similarity"] = float(score)
            results.append(item)
        return results

    def delete_document(self, document_id: str):
        new_metadata = [m for m in self.metadata if m["document_id"] != document_id]
        if len(new_metadata) == len(self.metadata):
            return
        self.metadata = new_metadata
        # rebuild index from scratch when removing documents
        self._create_index()
        # Embeddings are not persisted separately; require reload by reindexing if needed.
        self.save_index()
