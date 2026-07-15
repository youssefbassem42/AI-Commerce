from typing import Dict, Any, Optional
from pydantic import Field
from app.infrastructure.mongodb.documents.base_document import BaseMongoDocument
from app.domain.knowledge.entities.knowledge_chunk import KnowledgeChunk

class KnowledgeChunkDocument(BaseMongoDocument):
    """MongoDB document model representing a KnowledgeChunk."""
    document_id: str = Field(..., index=True)
    content: str = Field(...)
    chunk_index: int = Field(...)
    embedding_id: Optional[str] = Field(None, index=True)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    def to_entity(self) -> KnowledgeChunk:
        """Map document to domain Entity."""
        return KnowledgeChunk(
            id=str(self.id),
            document_id=self.document_id,
            content=self.content,
            chunk_index=self.chunk_index,
            embedding_id=self.embedding_id,
            metadata=self.metadata
        )

    @classmethod
    def from_entity(cls, entity: KnowledgeChunk) -> "KnowledgeChunkDocument":
        """Map domain Entity to MongoDB Document."""
        return cls(
            _id=entity.id,
            document_id=entity.document_id,
            content=entity.content,
            chunk_index=entity.chunk_index,
            embedding_id=entity.embedding_id,
            metadata=entity.metadata
        )
