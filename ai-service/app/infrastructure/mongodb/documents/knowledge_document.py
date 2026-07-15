from typing import List, Optional, Dict, Any
from pydantic import Field
from app.infrastructure.mongodb.documents.base_document import BaseMongoDocument
from app.infrastructure.mongodb.documents.knowledge_chunk_document import KnowledgeChunkDocument
from app.domain.knowledge.entities.knowledge_document import KnowledgeDocument

class KnowledgeDocumentModel(BaseMongoDocument):
    """MongoDB document model representing a KnowledgeDocument."""
    store_id: str = Field(..., index=True)
    title: str = Field(...)
    source_url: Optional[str] = Field(None)
    status: str = Field(default="processing")
    language: str = Field(...)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    chunks: Optional[List[KnowledgeChunkDocument]] = Field(default=None, exclude=True)
    chunking_strategy: str = Field(...)

    def to_entity(self) -> KnowledgeDocument:
        """Map document to domain Entity."""
        return KnowledgeDocument(
            id=str(self.id),
            store_id=self.store_id,
            title=self.title,
            source_url=self.source_url,
            status=self.status,
            language=self.language,
            metadata=self.metadata,
            chunks=[chk.to_entity() for chk in self.chunks] if self.chunks else [],
            chunking_strategy=self.chunking_strategy,
            created_at=self.created_at,
            updated_at=self.updated_at
        )

    @classmethod
    def from_entity(cls, entity: KnowledgeDocument) -> "KnowledgeDocumentModel":
        """Map domain Entity to MongoDB Document."""
        return cls(
            _id=entity.id,
            store_id=entity.store_id,
            title=entity.title,
            source_url=entity.source_url,
            status=entity.status,
            language=entity.language,
            metadata=entity.metadata,
            chunks=[KnowledgeChunkDocument.from_entity(chk) for chk in entity.chunks] if entity.chunks else [],
            chunking_strategy=entity.chunking_strategy,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )
