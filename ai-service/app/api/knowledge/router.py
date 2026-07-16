from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.application.knowledge.dto import (
    BusinessSummaryCreateDTO,
    BusinessSummaryUpdateDTO,
    KnowledgeChunkCreateDTO,
    KnowledgeChunkUpdateDTO,
    KnowledgeDocumentCreateDTO,
    KnowledgeDocumentUpdateDTO,
)
from app.application.knowledge.services import (
    BusinessSummaryService,
    KnowledgeChunkService,
    KnowledgeDocumentService,
)
from app.core.knowledge_settings import knowledge_settings
from app.domain.knowledge.exceptions import (
    BusinessSummaryNotFoundException,
    KnowledgeChunkNotFoundException,
    KnowledgeDocumentNotFoundException,
    KnowledgeDomainException,
)
from app.api.knowledge.dependencies import (
    get_business_summary_service,
    get_knowledge_chunk_service,
    get_knowledge_document_service,
)
from app.api.knowledge.schemas import (
    BusinessSummaryCreateSchema,
    BusinessSummaryResponseSchema,
    BusinessSummaryUpdateSchema,
    DeleteResponseSchema,
    KnowledgeChunkCreateSchema,
    KnowledgeChunkResponseSchema,
    KnowledgeChunkUpdateSchema,
    KnowledgeDocumentCreateSchema,
    KnowledgeDocumentResponseSchema,
    KnowledgeDocumentUpdateSchema,
    PaginatedBusinessSummaryResponseSchema,
    PaginatedKnowledgeChunkResponseSchema,
    PaginatedKnowledgeDocumentResponseSchema,
)

router = APIRouter(prefix=knowledge_settings.route_prefix, tags=["Knowledge Base"])


def _handle_exception(exc: Exception) -> None:
    if isinstance(
        exc,
        (
            KnowledgeDocumentNotFoundException,
            KnowledgeChunkNotFoundException,
            BusinessSummaryNotFoundException,
        ),
    ):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    if isinstance(exc, KnowledgeDomainException):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))


@router.post("/documents", response_model=KnowledgeDocumentResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_document(
    payload: KnowledgeDocumentCreateSchema,
    service: KnowledgeDocumentService = Depends(get_knowledge_document_service),
) -> KnowledgeDocumentResponseSchema:
    try:
        result = await service.create(KnowledgeDocumentCreateDTO(**payload.model_dump()))
        return KnowledgeDocumentResponseSchema(**result.model_dump())
    except Exception as exc:
        _handle_exception(exc)


@router.get("/documents/{document_id}", response_model=KnowledgeDocumentResponseSchema)
async def get_document(
    document_id: str,
    service: KnowledgeDocumentService = Depends(get_knowledge_document_service),
) -> KnowledgeDocumentResponseSchema:
    try:
        result = await service.get_by_id(document_id)
        return KnowledgeDocumentResponseSchema(**result.model_dump())
    except Exception as exc:
        _handle_exception(exc)


@router.get("/documents", response_model=PaginatedKnowledgeDocumentResponseSchema)
async def list_documents(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=knowledge_settings.default_page_size, ge=1, le=knowledge_settings.max_page_size),
    store_id: str | None = Query(default=None),
    status_filter: str | None = Query(default=None, alias="status"),
    service: KnowledgeDocumentService = Depends(get_knowledge_document_service),
) -> PaginatedKnowledgeDocumentResponseSchema:
    try:
        result = await service.list(page=page, page_size=page_size, store_id=store_id, status=status_filter)
        return PaginatedKnowledgeDocumentResponseSchema(**result.model_dump())
    except Exception as exc:
        _handle_exception(exc)


@router.put("/documents/{document_id}", response_model=KnowledgeDocumentResponseSchema)
async def update_document(
    document_id: str,
    payload: KnowledgeDocumentUpdateSchema,
    service: KnowledgeDocumentService = Depends(get_knowledge_document_service),
) -> KnowledgeDocumentResponseSchema:
    try:
        result = await service.update(document_id, KnowledgeDocumentUpdateDTO(**payload.model_dump(exclude_unset=True)))
        return KnowledgeDocumentResponseSchema(**result.model_dump())
    except Exception as exc:
        _handle_exception(exc)


@router.delete("/documents/{document_id}", response_model=DeleteResponseSchema)
async def delete_document(
    document_id: str,
    service: KnowledgeDocumentService = Depends(get_knowledge_document_service),
) -> DeleteResponseSchema:
    try:
        return DeleteResponseSchema(success=await service.delete(document_id))
    except Exception as exc:
        _handle_exception(exc)


@router.post("/chunks", response_model=KnowledgeChunkResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_chunk(
    payload: KnowledgeChunkCreateSchema,
    service: KnowledgeChunkService = Depends(get_knowledge_chunk_service),
) -> KnowledgeChunkResponseSchema:
    try:
        result = await service.create(KnowledgeChunkCreateDTO(**payload.model_dump()))
        return KnowledgeChunkResponseSchema(**result.model_dump())
    except Exception as exc:
        _handle_exception(exc)


@router.get("/chunks/{chunk_id}", response_model=KnowledgeChunkResponseSchema)
async def get_chunk(
    chunk_id: str,
    service: KnowledgeChunkService = Depends(get_knowledge_chunk_service),
) -> KnowledgeChunkResponseSchema:
    try:
        result = await service.get_by_id(chunk_id)
        return KnowledgeChunkResponseSchema(**result.model_dump())
    except Exception as exc:
        _handle_exception(exc)


@router.get("/chunks", response_model=PaginatedKnowledgeChunkResponseSchema)
async def list_chunks(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=knowledge_settings.default_page_size, ge=1, le=knowledge_settings.max_page_size),
    document_id: str | None = Query(default=None),
    version_number: int | None = Query(default=None, ge=1),
    service: KnowledgeChunkService = Depends(get_knowledge_chunk_service),
) -> PaginatedKnowledgeChunkResponseSchema:
    try:
        result = await service.list(page=page, page_size=page_size, document_id=document_id, version_number=version_number)
        return PaginatedKnowledgeChunkResponseSchema(**result.model_dump())
    except Exception as exc:
        _handle_exception(exc)


@router.put("/chunks/{chunk_id}", response_model=KnowledgeChunkResponseSchema)
async def update_chunk(
    chunk_id: str,
    payload: KnowledgeChunkUpdateSchema,
    service: KnowledgeChunkService = Depends(get_knowledge_chunk_service),
) -> KnowledgeChunkResponseSchema:
    try:
        result = await service.update(chunk_id, KnowledgeChunkUpdateDTO(**payload.model_dump(exclude_unset=True)))
        return KnowledgeChunkResponseSchema(**result.model_dump())
    except Exception as exc:
        _handle_exception(exc)


@router.delete("/chunks/{chunk_id}", response_model=DeleteResponseSchema)
async def delete_chunk(
    chunk_id: str,
    service: KnowledgeChunkService = Depends(get_knowledge_chunk_service),
) -> DeleteResponseSchema:
    try:
        return DeleteResponseSchema(success=await service.delete(chunk_id))
    except Exception as exc:
        _handle_exception(exc)


@router.post("/summaries", response_model=BusinessSummaryResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_summary(
    payload: BusinessSummaryCreateSchema,
    service: BusinessSummaryService = Depends(get_business_summary_service),
) -> BusinessSummaryResponseSchema:
    try:
        result = await service.create(BusinessSummaryCreateDTO(**payload.model_dump()))
        return BusinessSummaryResponseSchema(**result.model_dump())
    except Exception as exc:
        _handle_exception(exc)


@router.get("/summaries/{summary_id}", response_model=BusinessSummaryResponseSchema)
async def get_summary(
    summary_id: str,
    service: BusinessSummaryService = Depends(get_business_summary_service),
) -> BusinessSummaryResponseSchema:
    try:
        result = await service.get_by_id(summary_id)
        return BusinessSummaryResponseSchema(**result.model_dump())
    except Exception as exc:
        _handle_exception(exc)


@router.get("/summaries", response_model=PaginatedBusinessSummaryResponseSchema)
async def list_summaries(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=knowledge_settings.default_page_size, ge=1, le=knowledge_settings.max_page_size),
    document_id: str | None = Query(default=None),
    version_number: int | None = Query(default=None, ge=1),
    service: BusinessSummaryService = Depends(get_business_summary_service),
) -> PaginatedBusinessSummaryResponseSchema:
    try:
        result = await service.list(page=page, page_size=page_size, document_id=document_id, version_number=version_number)
        return PaginatedBusinessSummaryResponseSchema(**result.model_dump())
    except Exception as exc:
        _handle_exception(exc)


@router.put("/summaries/{summary_id}", response_model=BusinessSummaryResponseSchema)
async def update_summary(
    summary_id: str,
    payload: BusinessSummaryUpdateSchema,
    service: BusinessSummaryService = Depends(get_business_summary_service),
) -> BusinessSummaryResponseSchema:
    try:
        result = await service.update(summary_id, BusinessSummaryUpdateDTO(**payload.model_dump(exclude_unset=True)))
        return BusinessSummaryResponseSchema(**result.model_dump())
    except Exception as exc:
        _handle_exception(exc)


@router.delete("/summaries/{summary_id}", response_model=DeleteResponseSchema)
async def delete_summary(
    summary_id: str,
    service: BusinessSummaryService = Depends(get_business_summary_service),
) -> DeleteResponseSchema:
    try:
        return DeleteResponseSchema(success=await service.delete(summary_id))
    except Exception as exc:
        _handle_exception(exc)
