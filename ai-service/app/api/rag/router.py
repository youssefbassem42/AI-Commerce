import logging

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.rag.dependencies import get_rag_service
from app.api.rag.schemas import RAGChatRequestSchema, RAGChatResponseSchema
from app.application.rag.dto import RAGRequest
from app.application.rag.service import RagOrchestrationService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/rag", tags=["RAG Chat"])


@router.post("/chat", response_model=RAGChatResponseSchema)
async def rag_chat(
    payload: RAGChatRequestSchema,
    service: RagOrchestrationService = Depends(get_rag_service),
) -> RAGChatResponseSchema:
    try:
        request = RAGRequest(**payload.model_dump())
        result = await service.answer(request)

        return RAGChatResponseSchema(
            response=result.response,
            citations=[s.model_dump() for s in result.citations],
            chunk_references=[r.model_dump() for r in result.chunk_references],
            confidence_score=result.confidence_score,
            latency_ms=result.latency_ms,
            model=result.model,
            provider=result.provider,
            usage=result.usage.model_dump(),
            business_summary_version=result.business_summary_version,
            conversation_id=result.conversation_id,
        )
    except Exception as exc:
        logger.error("RAG chat failed: %s", exc, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"RAG chat failed: {exc}",
        )
