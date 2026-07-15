from app.domain.knowledge.entities.knowledge_document import KnowledgeDocument
from app.domain.knowledge.entities.knowledge_chunk import KnowledgeChunk
from app.infrastructure.mongodb.documents.knowledge_document import KnowledgeDocumentModel
from app.infrastructure.mongodb.documents.knowledge_chunk_document import KnowledgeChunkDocument
from app.application.knowledge.dto.knowledge_dto import KnowledgeDocumentDTO, KnowledgeChunkDTO

class KnowledgeMapper:
    """Maps Knowledge Aggregate between Mongo Documents, Domain Entities, and DTOs."""

    @staticmethod
    def to_entity(doc: KnowledgeDocumentModel) -> KnowledgeDocument:
        """Map Mongo Document to Domain Entity."""
        return doc.to_entity()

    @staticmethod
    def to_document(entity: KnowledgeDocument) -> KnowledgeDocumentModel:
        """Map Domain Entity to Mongo Document."""
        return KnowledgeDocumentModel.from_entity(entity)

    @staticmethod
    def to_dto(entity: KnowledgeDocument) -> KnowledgeDocumentDTO:
        """Map Domain Entity to DTO."""
        return KnowledgeDocumentDTO(
            id=entity.id,
            store_id=entity.store_id,
            title=entity.title,
            source_url=entity.source_url,
            status=entity.status,
            language=entity.language,
            metadata=entity.metadata,
            chunks=[
                KnowledgeChunkDTO(
                    id=chk.id,
                    document_id=chk.document_id,
                    content=chk.content,
                    chunk_index=chk.chunk_index,
                    embedding_id=chk.embedding_id,
                    metadata=chk.metadata
                )
                for chk in entity.chunks
            ],
            chunking_strategy=entity.chunking_strategy,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )
