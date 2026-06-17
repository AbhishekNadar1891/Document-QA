import logging
import uuid
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.api.schemas import ChatQueryRequest, ChatQueryResponse
from app.database.session import get_db
from app.database.models import Conversation, Message, Document
from app.services.retrieval_service import RetrievalService
from app.services.prompt_service import PromptService
from app.services.llm_service import LLMService
from app.services.embedding_service import EmbeddingService
from app.services.vector_store import VectorStore
from app.config.settings import settings

router = APIRouter()
logger = logging.getLogger(__name__)

vector_store = VectorStore()
embedder = EmbeddingService()
retriever = RetrievalService()
prompt_service = PromptService()
llm_service = LLMService()

@router.post("/query", response_model=ChatQueryResponse)
def query_chat(request: ChatQueryRequest, db: Session = Depends(get_db)):
    conversation_id = request.conversation_id or str(uuid.uuid4())
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not conversation:
        conversation = Conversation(id=conversation_id)
        db.add(conversation)
        db.commit()

    query_embedding = embedder.embed_query(request.question)
    retrieval = retriever.retrieve(request.question, query_embedding)

    context_text = prompt_service.build_context(retrieval["chunks"], conversation.messages)
    prompt = prompt_service.build_prompt(context_text, request.question)
    answer = llm_service.generate(prompt)

    message_user = Message(conversation_id=conversation_id, role="user", content=request.question)
    message_assistant = Message(conversation_id=conversation_id, role="assistant", content=answer)
    db.add_all([message_user, message_assistant])
    db.commit()

    sources = [
        {"document": item["document_id"], "page_number": item["page_number"], "similarity": item["similarity"], "chunk_id": item["chunk_id"]}
        for item in retrieval["sources"]
    ]

    logger.info("Chat query processed for conversation %s", conversation_id)
    return {"answer": answer, "sources": sources, "conversation_id": conversation_id}

@router.post("/stream")
def stream_chat(request: ChatQueryRequest, db: Session = Depends(get_db)):
    conversation_id = request.conversation_id or str(uuid.uuid4())
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not conversation:
        conversation = Conversation(id=conversation_id)
        db.add(conversation)
        db.commit()

    query_embedding = embedder.embed_query(request.question)
    retrieval = retriever.retrieve(request.question, query_embedding)
    context_text = prompt_service.build_context(retrieval["chunks"], conversation.messages)
    prompt = prompt_service.build_prompt(context_text, request.question)

    def event_generator():
        for token in llm_service.stream_generate(prompt):
            yield f"data: {token}\n\n"

    logger.info("Streaming chat initiated for conversation %s", conversation_id)
    return StreamingResponse(event_generator(), media_type="text/event-stream")
