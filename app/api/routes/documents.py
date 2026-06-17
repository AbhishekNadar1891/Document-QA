import os
import uuid
import logging
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.config.settings import settings
from app.database.session import get_db
from app.database.models import Document, Chunk
from app.services.parsers.pdf_parser import parse_pdf
from app.services.parsers.docx_parser import parse_docx
from app.services.parsers.txt_parser import parse_txt
from app.services.chunking_service import ChunkingService
from app.services.embedding_service import EmbeddingService
from app.services.vector_store import VectorStore

router = APIRouter()
logger = logging.getLogger(__name__)

vector_store = VectorStore()
chunker = ChunkingService()
embedder = EmbeddingService()

PARSER_BY_EXTENSION = {
    "pdf": parse_pdf,
    "docx": parse_docx,
    "txt": parse_txt,
}

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    filename = file.filename
    if not filename or "." not in filename:
        raise HTTPException(status_code=400, detail="Filename missing or unsupported")

    extension = filename.rsplit(".", 1)[-1].lower()
    if extension not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=415, detail="Unsupported file type")

    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Empty file")
    if len(content) > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(status_code=413, detail="File too large")

    document_id = str(uuid.uuid4())
    os.makedirs(settings.DATA_DIR / "uploads", exist_ok=True)
    saved_path = settings.DATA_DIR / "uploads" / f"{document_id}.{extension}"
    with open(saved_path, "wb") as f:
        f.write(content)

    parser = PARSER_BY_EXTENSION[extension]
    document_text = parser(saved_path)

    chunks = chunker.chunk_text(
        document_id=document_id,
        text=document_text["content"],
        pages=document_text.get("pages", []),
        chunk_size=settings.PAGE_SIZE,
        chunk_overlap=settings.PAGE_OVERLAP,
    )

    embeddings = embedder.embed_documents([chunk["text"] for chunk in chunks])
    vector_store.add_vectors(chunks, embeddings)

    doc = Document(id=document_id, filename=filename, total_chunks=len(chunks))
    db.add(doc)
    db.commit()

    db_chunks = [
        Chunk(
            document_id=document_id,
            chunk_id=chunk["chunk_id"],
            page_number=chunk["page_number"],
            text=chunk["text"],
            token_count=chunk["token_count"],
        )
        for chunk in chunks
    ]
    db.add_all(db_chunks)
    db.commit()

    logger.info("Uploaded document %s with %s chunks", filename, len(chunks))
    return JSONResponse({
        "document_id": document_id,
        "filename": filename,
        "chunks_created": len(chunks),
        "status": "indexed",
    })

@router.get("")
def list_documents(db: Session = Depends(get_db)):
    documents = db.query(Document).all()
    return [
        {"id": item.id, "filename": item.filename, "upload_date": item.upload_date, "total_chunks": item.total_chunks}
        for item in documents
    ]

@router.get("/{document_id}")
def get_document(document_id: str, db: Session = Depends(get_db)):
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return {
        "id": document.id,
        "filename": document.filename,
        "upload_date": document.upload_date,
        "total_chunks": document.total_chunks,
        "chunks": [
            {
                "chunk_id": chunk.chunk_id,
                "page_number": chunk.page_number,
                "text": chunk.text,
                "token_count": chunk.token_count,
            }
            for chunk in document.chunks
        ],
    }

@router.delete("/{document_id}")
def delete_document(document_id: str, db: Session = Depends(get_db)):
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    db.query(Chunk).filter(Chunk.document_id == document_id).delete()
    db.delete(document)
    db.commit()

    vector_store.delete_document(document_id)
    upload_dir = settings.DATA_DIR / "uploads"
    for ext in settings.ALLOWED_EXTENSIONS:
        candidate = upload_dir / f"{document_id}.{ext}"
        if candidate.exists():
            candidate.unlink()

    logger.info("Deleted document %s", document_id)
    return {"status": "deleted"}
