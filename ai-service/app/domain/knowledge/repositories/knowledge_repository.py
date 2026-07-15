from abc import ABC, abstractmethod
from typing import List, Optional
from app.shared.kernel.repository import AsyncRepository
from app.domain.knowledge.entities.knowledge_document import KnowledgeDocument
from app.domain.knowledge.entities.knowledge_chunk import KnowledgeChunk

class KnowledgeRepository(AsyncRepository[KnowledgeDocument, str], ABC):
    """Domain repository interface for KnowledgeDocument Aggregate."""

    @abstractmethod
    async def find_by_store_id(self, store_id: str, limit: int = 20, skip: int = 0) -> List[KnowledgeDocument]:
        """Find knowledge documents belonging to a store."""
        pass

    @abstractmethod
    async def add_chunks(self, document_id: str, chunks: List[KnowledgeChunk]) -> bool:
        """Add list of chunks to a knowledge document."""
        pass
