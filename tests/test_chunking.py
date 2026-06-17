from app.services.chunking_service import ChunkingService


def test_chunking_preserves_sentences():
    service = ChunkingService()
    text = "This is sentence one. This is sentence two. This is sentence three."
    chunks = service.chunk_text("doc1", text, [], chunk_size=30, chunk_overlap=10)
    assert len(chunks) >= 1
    assert all("." in chunk["text"] for chunk in chunks)
    assert sum(len(chunk["text"].split()) for chunk in chunks) >= 9
