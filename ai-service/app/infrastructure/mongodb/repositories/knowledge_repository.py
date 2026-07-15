from typing import List, Optional, Any
from bson import ObjectId
import logging

from app.domain.knowledge.entities.knowledge_document import KnowledgeDocument
from app.domain.knowledge.entities.knowledge_chunk import KnowledgeChunk
from app.domain.knowledge.repositories.knowledge_repository import KnowledgeRepository as IKnowledgeRepository
from app.infrastructure.mongodb.repositories.base_repository import BaseMongoRepository
from app.infrastructure.mongodb.documents.knowledge_document import KnowledgeDocumentModel
from app.infrastructure.mongodb.documents.knowledge_chunk_document import KnowledgeChunkDocument
from app.infrastructure.mongodb.collections import get_knowledge_documents_collection, get_knowledge_chunks_collection

logger = logging.getLogger(__name__)

class KnowledgeRepository(BaseMongoRepository[KnowledgeDocumentModel, KnowledgeDocument], IKnowledgeRepository):
    """MongoDB implementation of the KnowledgeRepository with transaction and session support."""

    def __init__(self):
        super().__init__(get_knowledge_documents_collection(), KnowledgeDocumentModel)
        self.chunks_collection = get_knowledge_chunks_collection()

    async def create(self, entity: KnowledgeDocument, session: Any = None) -> KnowledgeDocument:
        """Create a knowledge document along with its chunks atomically."""
        try:
            await super().create(entity, session=session)
            if entity.chunks:
                chunk_docs = [KnowledgeChunkDocument.from_entity(c).to_mongo_dict() for c in entity.chunks]
                await self.chunks_collection.insert_many(chunk_docs, session=session)
            return entity
        except Exception as e:
            self._handle_db_error(e)
            raise

    async def update(self, entity: KnowledgeDocument, session: Any = None) -> KnowledgeDocument:
        """Update a knowledge document and sync its chunks atomically."""
        try:
            await super().update(entity, session=session)
            await self.chunks_collection.delete_many({"document_id": entity.id}, session=session)
            if entity.chunks:
                chunk_docs = [KnowledgeChunkDocument.from_entity(c).to_mongo_dict() for c in entity.chunks]
                await self.chunks_collection.insert_many(chunk_docs, session=session)
            return entity
        except Exception as e:
            self._handle_db_error(e)
            raise

    async def find_by_id(self, id: str, session: Any = None) -> Optional[KnowledgeDocument]:
        """Find a knowledge document by ID and load its chunks."""
        try:
            doc = await super().find_by_id(id, session=session)
            if not doc:
                return None
            
            cursor = self.chunks_collection.find(
                {"document_id": id}, 
                session=session
            ).sort("chunk_index", 1)
            
            chunks = []
            async for data in cursor:
                chunk_doc = KnowledgeChunkDocument.from_mongo_dict(data)
                chunks.append(chunk_doc.to_entity())
            doc.chunks = chunks
            return doc
        except Exception as e:
            self._handle_db_error(e)
            raise

    async def find_by_store_id(
        self, store_id: str, limit: int = 20, skip: int = 0, session: Any = None
    ) -> List[KnowledgeDocument]:
        """Retrieve documents belonging to a store with chunks populated."""
        try:
            docs = await self.find_many(
                {"store_id": store_id}, 
                limit=limit, 
                skip=skip, 
                session=session
            )
            for doc in docs:
                cursor = self.chunks_collection.find(
                    {"document_id": doc.id}, 
                    session=session
                ).sort("chunk_index", 1)
                
                chunks = []
                async for data in cursor:
                    chunk_doc = KnowledgeChunkDocument.from_mongo_dict(data)
                    chunks.append(chunk_doc.to_entity())
                doc.chunks = chunks
            return docs
        except Exception as e:
            self._handle_db_error(e)
            raise

    async def add_chunks(self, document_id: str, chunks: List[KnowledgeChunk], session: Any = None) -> bool:
        """Add chunks to an existing document."""
        if not chunks:
            return True
        try:
            chunk_docs = [KnowledgeChunkDocument.from_entity(c).to_mongo_dict() for c in chunks]
            await self.chunks_collection.insert_many(chunk_docs, session=session)
            return True
        except Exception as e:
            self._handle_db_error(e)
            raise
