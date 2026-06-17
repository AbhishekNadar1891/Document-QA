# HybridRAG Platform

A production-ready Retrieval-Augmented Generation (RAG) backend for intelligent document understanding and question answering.

The platform enables users to upload documents, perform semantic search, and interact with them through natural language queries using Large Language Models (LLMs). It combines vector-based retrieval with LLM reasoning to generate context-aware responses grounded in the uploaded knowledge base.

---

## Overview

Traditional LLMs cannot access private or domain-specific documents without retraining. Retrieval-Augmented Generation (RAG) solves this problem by retrieving relevant information from a document corpus and providing it as context to the language model at inference time.

This project implements a complete enterprise-style RAG pipeline including:

* Document ingestion
* Text extraction
* Intelligent chunking
* Semantic embedding generation
* FAISS vector indexing
* Similarity-based retrieval
* Prompt construction
* LLM-powered answer generation
* Source attribution

---

## Key Features

### Document Processing

* PDF support
* DOCX support
* TXT support
* Metadata preservation
* Automatic text extraction

### Semantic Retrieval

* Sentence Transformer embeddings
* FAISS vector database
* Top-K similarity search
* Persistent vector storage
* Multi-document retrieval

### Question Answering

* Retrieval-Augmented Generation pipeline
* Context-aware answers
* Source citations
* Conversation memory
* Multi-turn interactions

### API Support

* REST API using FastAPI
* OpenAPI / Swagger documentation
* Server-Sent Events (SSE) streaming
* Structured request and response schemas

### Production Features

* Docker deployment
* Environment-based configuration
* Logging
* SQLite metadata storage
* Unit testing
* Modular architecture

---

## System Architecture

```text
User Query
    │
    ▼
FastAPI API Layer
    │
    ▼
Embedding Service
    │
    ▼
FAISS Vector Store
    │
    ▼
Top-K Retrieval
    │
    ▼
Prompt Builder
    │
    ▼
LLM Service
    │
    ▼
Generated Answer
```

### Document Ingestion Flow

```text
Document Upload
      │
      ▼
Text Extraction
      │
      ▼
Chunking
      │
      ▼
Embedding Generation
      │
      ▼
FAISS Indexing
      │
      ▼
Persistent Storage
```

---

## Technology Stack

### Backend

* Python 3.12
* FastAPI
* Pydantic

### Machine Learning

* Sentence Transformers
* FAISS
* NumPy

### Database

* SQLite
* SQLAlchemy

### LLM Integration

* OpenAI API
* OpenRouter API

### DevOps

* Docker
* Docker Compose
* Git

### Testing

* Pytest

---

## Project Structure

```text
app/
│
├── api/
│   ├── routes/
│   │   ├── chat.py
│   │   ├── documents.py
│   │   └── search.py
│
├── config/
│   └── settings.py
│
├── database/
│   ├── models.py
│   └── session.py
│
├── services/
│   ├── parsers/
│   ├── embedding_service.py
│   ├── chunking_service.py
│   ├── vector_store.py
│   ├── retrieval_service.py
│   ├── prompt_service.py
│   └── llm/
│
├── utils/
│
└── main.py
```

---

## Installation

### Clone Repository

```bash
git clone https://github.com/AbhishekNadar1891/Document-QA.git

cd Document-QA
```

### Create Environment

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

Linux/macOS:

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file:

```env
OPENAI_API_KEY=your_key_here

OPENROUTER_API_KEY=your_key_here

EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

TOP_K=5
```

---

## Running Locally

```bash
uvicorn app.main:app --reload
```

API Documentation:

```text
http://localhost:8000/docs
```

---

## Running with Docker

```bash
docker compose up --build
```

---

## API Endpoints

### Upload Document

```http
POST /documents/upload
```

Upload PDF, DOCX, or TXT files.

---

### List Documents

```http
GET /documents
```

Retrieve indexed documents.

---

### Document Details

```http
GET /documents/{id}
```

Retrieve metadata and associated chunks.

---

### Delete Document

```http
DELETE /documents/{id}
```

Remove document and embeddings.

---

### Semantic Search

```http
POST /search
```

Search documents using vector similarity.

---

### Ask Questions

```http
POST /chat/query
```

Generate answers using retrieved context.

---

### Streaming Responses

```http
POST /chat/stream
```

Receive answers as a token stream.

---

## Testing

Run all tests:

```bash
pytest
```

---

## Future Improvements

* Hybrid Retrieval (BM25 + FAISS)
* Cross Encoder Re-ranking
* PostgreSQL Support
* Role-Based Access Control
* User Authentication
* LangGraph Agents
* Knowledge Graph Integration
* Milvus / Pinecone Migration
* Multi-tenant Architecture

---

## Resume Highlights

* Built a production-ready Retrieval-Augmented Generation platform using FastAPI, FAISS, and LLM APIs.
* Implemented semantic document retrieval using Sentence Transformers and vector similarity search.
* Developed scalable REST APIs for document ingestion, indexing, retrieval, and question answering.
* Designed a modular architecture supporting future enterprise upgrades such as hybrid retrieval and agentic workflows.

---

## License

This project is intended for educational, research, and portfolio purposes.
