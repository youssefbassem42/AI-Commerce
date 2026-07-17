import logging
import time
from typing import Optional

from app.application.dto.ai_dto import ChatRequest as AIChatRequest, MessageDTO, UsageDTO
from app.application.knowledge.retrieval import RetrieverService
from app.application.knowledge.retrieval.config import RetrievalConfig, RetrievalFilters
from app.application.rag.dedup import deduplicate_chunks
from app.application.rag.dto import ChunkReference, Citation, RAGRequest, RAGResponse
from app.application.rag.prompt import build_rag_messages
from app.application.services.chat_service import ChatService
from app.application.services.conversation_service import ConversationService
from app.core.ai_settings import ai_settings
from app.core.model_registry import ModelRegistry
from app.domain.knowledge.repositories.business_summary_repository import BusinessSummaryRepository

logger = logging.getLogger(__name__)

MAX_CHUNK_CHARS = 2000
MAX_CHUNKS_IN_CONTEXT = 10


class RagOrchestrationService:
    def __init__(
        self,
        retriever_service: RetrieverService,
        chat_service: ChatService,
        conversation_service: Optional[ConversationService] = None,
        business_summary_repository: Optional[BusinessSummaryRepository] = None,
    ):
        self._retriever = retriever_service
        self._chat = chat_service
        self._conversation_service = conversation_service
        self._summary_repo = business_summary_repository

    async def answer(self, request: RAGRequest) -> RAGResponse:
        start = time.perf_counter()
        model = request.model or ai_settings.DEFAULT_MODEL

        retrieval_config = RetrievalConfig(
            top_k=min(request.top_k, MAX_CHUNKS_IN_CONTEXT),
            score_threshold=request.score_threshold,
            use_hybrid=request.use_hybrid,
            use_mmr=request.use_mmr,
            rerank=request.rerank,
        )

        retrieval_filters = RetrievalFilters(
            organization_id=request.organization_id,
            store_id=request.store_id,
            language=request.language,
            knowledge_scope=request.knowledge_scope,
        )

        retrieval_result = await self._retriever.search(
            query=request.message,
            filters=retrieval_filters,
            config=retrieval_config,
        )

        chunks = deduplicate_chunks(retrieval_result.results)
        chunk_refs = [
            ChunkReference(
                chunk_id=c.chunk_id,
                document_id=c.document_id,
                document_title=c.document_title,
                content_snippet=c.content[:200],
                score=c.score,
                rank=c.rank,
            )
            for c in chunks
        ]

        business_summary_text = None
        business_summary_version = None

        if self._summary_repo:
            try:
                summaries = await self._summary_repo.find_by_document_id(
                    document_id=request.store_id,
                )
                if summaries:
                    latest = max(summaries, key=lambda s: (s.version_number, s.created_at))
                    business_summary_text = latest.summary
                    business_summary_version = latest.version_number
            except Exception:
                logger.warning("Failed to load business summary for store '%s'", request.store_id, exc_info=True)

        chunks_context_lines = []
        for i, c in enumerate(chunks[:MAX_CHUNKS_IN_CONTEXT]):
            snippet = c.content[:MAX_CHUNK_CHARS]
            chunks_context_lines.append(
                f"\n### Retrieved Knowledge Chunk [{i + 1}]\n"
                f"**Source:** {c.document_title}\n"
                f"{snippet}\n"
            )

        chunks_context = "\n".join(chunks_context_lines)

        system_content, user_content, _ = build_rag_messages(
            user_message=request.message,
            chunks_context=chunks_context,
            business_summary_context=business_summary_text,
            business_summary_version=business_summary_version,
        )

        messages = [MessageDTO(role="system", content=system_content)]

        if request.conversation_id and self._conversation_service:
            try:
                history = await self._conversation_service.get_conversation_history(
                    request.conversation_id,
                )
                if history:
                    messages.extend(history)
            except Exception:
                logger.warning("Failed to load conversation history for '%s'", request.conversation_id)

        messages.append(MessageDTO(role="user", content=user_content))

        ai_request = AIChatRequest(
            messages=messages,
            model=model,
            temperature=request.temperature or 0.3,
            max_tokens=request.max_tokens or 1024,
        )

        chat_latency_start = time.perf_counter()
        llm_response = await self._chat.chat(
            request=ai_request,
            conversation_id=request.conversation_id,
        )
        chat_latency = (time.perf_counter() - chat_latency_start) * 1000

        response_text = llm_response.message.content
        if isinstance(response_text, list):
            response_text = " ".join(str(item) for item in response_text)

        citations = self._extract_citations(response_text, chunks[:MAX_CHUNKS_IN_CONTEXT])
        confidence = self._calculate_confidence(chunks, business_summary_text is not None)

        total_latency = (time.perf_counter() - start) * 1000
        model_info = ModelRegistry.get_model_info(model)

        return RAGResponse(
            response=response_text,
            citations=citations,
            chunk_references=chunk_refs,
            confidence_score=confidence,
            latency_ms=total_latency,
            model=llm_response.model or model,
            provider=llm_response.provider or (model_info.provider if model_info else "unknown"),
            usage=llm_response.usage,
            business_summary_version=business_summary_version,
            conversation_id=request.conversation_id,
        )

    def _extract_citations(
        self,
        text: str,
        chunks: list,
    ) -> list[Citation]:
        import re

        citations: list[Citation] = []
        seen: set[int] = set()

        for match in re.finditer(r"\[citation:(\d+)\]", text):
            idx = int(match.group(1))
            if idx in seen:
                continue
            seen.add(idx)

            if 1 <= idx <= len(chunks):
                c = chunks[idx - 1]
                citations.append(Citation(
                    index=idx,
                    chunk_id=c.chunk_id,
                    document_title=c.document_title,
                    content_snippet=c.content[:200],
                    score=c.score,
                    rank=c.rank,
                ))

        return citations

    def _calculate_confidence(
        self,
        chunks: list,
        has_business_summary: bool,
    ) -> float:
        if not chunks:
            return 0.0

        top_k = min(5, len(chunks))
        avg_score = sum(c.score for c in chunks[:top_k]) / top_k

        if has_business_summary:
            confidence = 0.3 + 0.7 * avg_score
        else:
            confidence = 0.2 + 0.8 * avg_score

        return max(0.0, min(1.0, confidence))
