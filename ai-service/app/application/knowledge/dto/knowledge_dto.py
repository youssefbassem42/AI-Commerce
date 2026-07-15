from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel

class KnowledgeChunkDTO(BaseModel):
    id: str
    document_id: str
    content: str
    chunk_index: int
    embedding_id: Optional[str] = None
    metadata: Dict[str, Any]

class KnowledgeDocumentDTO(BaseModel):
    id: str
    store_id: str
    title: str
    source_url: Optional[str] = None
    status: str
    language: str
    metadata: Dict[str, Any]
    chunks: List[KnowledgeChunkDTO]
    chunking_strategy: str
    created_at: datetime
    updated_at: datetime
