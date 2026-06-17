# RAG Platform

Enterprise-grade Retrieval-Augmented Generation backend built with FastAPI, FAISS, and OpenAI/OpenRouter.

## Architecture

- FastAPI REST API
- Document parsers for PDF, DOCX, TXT
- Sentence-preserving chunking
- Sentence Transformers embeddings
- FAISS semantic vector store
- SQLite metadata storage
- Conversation memory with chat history
- SSE streaming endpoint
- Docker and Docker Compose deployment

## Features

- Document upload `/documents/upload`
- Semantic search `/search`
- Question answering `/chat/query`
- Streaming responses `/chat/stream`
- Document management

## Setup

1. Copy `.env.example` to `.env`
2. Set `OPENAI_API_KEY` or `OPENROUTER_API_KEY`
3. Build and run:

```bash
docker compose up --build
```

## API Endpoints

- `POST /documents/upload` - upload a PDF, DOCX or TXT document
- `GET /documents` - list uploaded documents
- `GET /documents/{id}` - document details + chunks
- `DELETE /documents/{id}` - delete document and associated embeddings
- `POST /search` - semantic search
- `POST /chat/query` - answer a question using uploaded documents
- `POST /chat/stream` - stream an answer as SSE

## Project Structure

- `app/` - application code
- `app/api/routes/` - FastAPI route implementations
- `app/services/` - parsers, chunking, embeddings, vector store, retrieval, prompt and LLM
- `app/database/` - SQLAlchemy models and DB session
- `data/` - persisted vector store and SQLite data
- `logs/` - application logs

## Notes

- Designed for future enterprise upgrades: hybrid search, reranking, RBAC, PostgreSQL, Milvus migration.
- Vector metadata is stored in `data/vectorstore/metadata.json` and FAISS index at `data/vectorstore/faiss.index`.
