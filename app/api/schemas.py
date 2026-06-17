from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

class DocumentUploadResponse(BaseModel):
    document_id: str
    filename: str
    chunks_created: int
    status: str

class DocumentMetadata(BaseModel):
    id: str
    filename: str
    upload_date: datetime
    total_chunks: int

    class Config:
        orm_mode = True

class ChunkMetadata(BaseModel):
    chunk_id: str
    page_number: Optional[int]
    text: str
    token_count: int

    class Config:
        orm_mode = True

class DocumentDetailResponse(DocumentMetadata):
    chunks: List[ChunkMetadata]

class SourceItem(BaseModel):
    document: str
    page_number: Optional[int]
    similarity: float
    chunk_id: str

class ChatQueryRequest(BaseModel):
    question: str = Field(..., min_length=1)
    conversation_id: Optional[str] = None

class ChatQueryResponse(BaseModel):
    answer: str
    sources: List[SourceItem]
    conversation_id: Optional[str]

class SearchRequest(BaseModel):
    query: str = Field(..., min_length=1)

class SearchResult(BaseModel):
    document_id: str
    filename: str
    chunk_id: str
    page_number: Optional[int]
    text: str
    similarity: float

class SearchResponse(BaseModel):
    results: List[SearchResult]

class ConversationCreateResponse(BaseModel):
    conversation_id: str

class MessageResponse(BaseModel):
    role: str
    content: str
    created_at: datetime
