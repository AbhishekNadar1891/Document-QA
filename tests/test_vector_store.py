import numpy as np
from app.services.vector_store import VectorStore


def test_vector_store_add_and_search(tmp_path, monkeypatch):
    metadata_file = tmp_path / "metadata.json"
    index_file = tmp_path / "faiss.index"

    class DummySettings:
        VECTOR_INDEX_FILE = index_file
        VECTOR_METADATA_FILE = metadata_file

    monkeypatch.setattr("app.services.vector_store.settings", DummySettings)

    store = VectorStore()
    store.dimension = 3
    store._create_index()
    store.add_vectors([
        {"document_id": "doc1", "chunk_id": "1", "page_number": 1, "text": "test"}
    ], [[1.0, 0.0, 0.0]])
    results = store.search([1.0, 0.0, 0.0], top_k=1)

    assert len(results) == 1
    assert results[0]["document_id"] == "doc1"
    assert results[0]["similarity"] == 1.0
