from fastapi import Depends

from app.application.knowledge.services import (
    BusinessSummaryService,
    KnowledgeChunkService,
    KnowledgeDocumentService,
)
from app.infrastructure.mongodb.repositories.business_summary_repository import (
    BusinessSummaryRepository,
)
from app.infrastructure.mongodb.repositories.chunk_repository import ChunkRepository
from app.infrastructure.mongodb.repositories.knowledge_repository import KnowledgeRepository


def get_knowledge_repository() -> KnowledgeRepository:
    return KnowledgeRepository()


def get_chunk_repository() -> ChunkRepository:
    return ChunkRepository()


def get_business_summary_repository() -> BusinessSummaryRepository:
    return BusinessSummaryRepository()


def get_knowledge_document_service(
    repository: KnowledgeRepository = Depends(get_knowledge_repository),
) -> KnowledgeDocumentService:
    return KnowledgeDocumentService(repository=repository)


def get_knowledge_chunk_service(
    repository: ChunkRepository = Depends(get_chunk_repository),
) -> KnowledgeChunkService:
    return KnowledgeChunkService(repository=repository)


def get_business_summary_service(
    repository: BusinessSummaryRepository = Depends(get_business_summary_repository),
) -> BusinessSummaryService:
    return BusinessSummaryService(repository=repository)
