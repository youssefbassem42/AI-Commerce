from typing import Dict, Any, Optional
from pydantic import Field
from app.shared.kernel.entity import Entity

class KnowledgeChunk(Entity[str]):
    """Domain representation of a portion of a knowledge document."""
    document_id: str = Field(..., description="ID of the parent KnowledgeDocument")
    content: str = Field(..., description="Text content of this chunk")
    chunk_index: int = Field(..., description="Sequential index of this chunk within the document")
    embedding_id: Optional[str] = Field(None, description="Vector database identifier/index ID")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Arbitrary metadata for RAG filtering")
