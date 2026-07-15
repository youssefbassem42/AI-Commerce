from datetime import datetime, UTC
from typing import List, Optional
from pydantic import Field
from app.shared.kernel.aggregate_root import AggregateRoot
from app.domain.knowledge.entities.knowledge_chunk import KnowledgeChunk

class KnowledgeDocument(AggregateRoot[str]):
    """Domain Aggregate Root representing a knowledge document (e.g. FAQ, product manual)."""
    store_id: str = Field(..., description="Commerce store context ID")
    title: str = Field(..., description="Title of the document")
    source_url: Optional[str] = Field(None, description="URL source of the document if applicable")
    status: str = Field(default="processing", description="Status (processing, active, error)")
    language: str = Field(..., description="Language of the document")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Metadata associated with the document")
    chunks: List[KnowledgeChunk] = Field(default_factory=list, description="Associated document chunks")
    chunking_strategy: str = Field(..., description="Strategy used for chunking the document")
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
