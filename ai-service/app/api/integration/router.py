import logging

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status

from app.api.integration.dependencies import get_integration_service, get_sync_orchestrator
from app.api.integration.schemas import (
    ConnectionResponseSchema,
    CreateConnectionSchema,
    DeleteResponseSchema,
    PaginatedConnectionResponseSchema,
    ParseSpecRequestSchema,
    ParseSpecResponseSchema,
    SyncRequestSchema,
    SyncResponseSchema,
    UpdateCredentialsSchema,
    UpdateMappingsSchema,
)
from app.application.integration.mapping.dto import (
    AuthConfigDTO,
    ConnectionCreateDTO,
    ConnectionUpdateCredentialsDTO,
    ConnectionUpdateMappingsDTO,
    EntityMappingDTO,
    FieldMappingDTO,
    PaginationConfigDTO,
    ParseSpecRequestDTO,
)
from app.application.integration.mapping.services import IntegrationApplicationService
from app.application.integration.sync.orchestrator import SyncOrchestrator
from app.domain.integration.exceptions import (
    DuplicateConnectionException,
    IntegrationConnectionNotFoundException,
    IntegrationDomainException,
    IntegrationValidationException,
    InvalidMappingException,
    InvalidSpecException,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/integration", tags=["Integration"])


def _handle_exception(exc: Exception) -> None:
    if isinstance(exc, IntegrationConnectionNotFoundException):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    if isinstance(exc, (IntegrationValidationException, InvalidMappingException, InvalidSpecException)):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
    if isinstance(exc, DuplicateConnectionException):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))
    if isinstance(exc, IntegrationDomainException):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
    logger.exception("Unhandled integration error")
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@router.post("/schemas/parse", response_model=ParseSpecResponseSchema, status_code=status.HTTP_200_OK)
async def parse_spec(
    payload: ParseSpecRequestSchema,
    request: Request,
    service: IntegrationApplicationService = Depends(get_integration_service),
) -> ParseSpecResponseSchema:
    try:
        dto = ParseSpecRequestDTO(
            platform_name=payload.platform_name,
            raw_spec=payload.raw_spec,
        )
        result = await service.parse_spec(dto)
        return ParseSpecResponseSchema(**result.model_dump())
    except Exception as exc:
        _handle_exception(exc)


@router.post("/connections", response_model=ConnectionResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_connection(
    payload: CreateConnectionSchema,
    request: Request,
    service: IntegrationApplicationService = Depends(get_integration_service),
) -> ConnectionResponseSchema:
    try:
        organization_id = getattr(request.state, "tenant_id", payload.store_id)
        dto = ConnectionCreateDTO(
            store_id=payload.store_id,
            organization_id=organization_id,
            name=payload.name,
            platform_name=payload.platform_name,
            raw_spec=payload.raw_spec,
            auth_config=AuthConfigDTO(**payload.auth_config.model_dump()),
            credentials=payload.credentials,
            entity_mappings=[
                EntityMappingDTO(
                    entity_type=em.entity_type,
                    list_path=em.list_path,
                    list_method=em.list_method,
                    detail_path=em.detail_path,
                    detail_method=em.detail_method,
                    id_field=em.id_field,
                    pagination=PaginationConfigDTO(**em.pagination.model_dump()),
                    field_mappings=[FieldMappingDTO(**fm.model_dump()) for fm in em.field_mappings],
                )
                for em in payload.entity_mappings
            ],
        )
        result = await service.create_connection(dto)
        return ConnectionResponseSchema(**result.model_dump())
    except Exception as exc:
        _handle_exception(exc)


@router.get("/connections", response_model=PaginatedConnectionResponseSchema)
async def list_connections(
    request: Request,
    store_id: str = Query(...),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    service: IntegrationApplicationService = Depends(get_integration_service),
) -> PaginatedConnectionResponseSchema:
    try:
        items, total = await service.list_connections(
            store_id=store_id, page=page, page_size=page_size
        )
        return PaginatedConnectionResponseSchema(
            items=[ConnectionResponseSchema(**item.model_dump()) for item in items],
            total=total,
            page=page,
            page_size=page_size,
        )
    except Exception as exc:
        _handle_exception(exc)


@router.get("/connections/{connection_id}", response_model=ConnectionResponseSchema)
async def get_connection(
    connection_id: str,
    service: IntegrationApplicationService = Depends(get_integration_service),
) -> ConnectionResponseSchema:
    try:
        result = await service.get_connection(connection_id)
        return ConnectionResponseSchema(**result.model_dump())
    except Exception as exc:
        _handle_exception(exc)


@router.put("/connections/{connection_id}/mappings", response_model=ConnectionResponseSchema)
async def update_connection_mappings(
    connection_id: str,
    payload: UpdateMappingsSchema,
    service: IntegrationApplicationService = Depends(get_integration_service),
) -> ConnectionResponseSchema:
    try:
        result = await service.update_mappings(
            connection_id=connection_id,
            entity_mappings=[
                EntityMappingDTO(
                    entity_type=em.entity_type,
                    list_path=em.list_path,
                    list_method=em.list_method,
                    detail_path=em.detail_path,
                    detail_method=em.detail_method,
                    id_field=em.id_field,
                    pagination=PaginationConfigDTO(**em.pagination.model_dump()),
                    field_mappings=[FieldMappingDTO(**fm.model_dump()) for fm in em.field_mappings],
                )
                for em in payload.entity_mappings
            ],
        )
        return ConnectionResponseSchema(**result.model_dump())
    except Exception as exc:
        _handle_exception(exc)


@router.put("/connections/{connection_id}/credentials", response_model=ConnectionResponseSchema)
async def update_connection_credentials(
    connection_id: str,
    payload: UpdateCredentialsSchema,
    service: IntegrationApplicationService = Depends(get_integration_service),
) -> ConnectionResponseSchema:
    try:
        result = await service.update_credentials(
            connection_id=connection_id,
            auth_config_dto=AuthConfigDTO(**payload.auth_config.model_dump()),
            credentials=payload.credentials,
        )
        return ConnectionResponseSchema(**result.model_dump())
    except Exception as exc:
        _handle_exception(exc)


@router.post("/connections/{connection_id}/sync", response_model=SyncResponseSchema, status_code=status.HTTP_200_OK)
async def sync_connection(
    connection_id: str,
    payload: SyncRequestSchema,
    orchestrator: SyncOrchestrator = Depends(get_sync_orchestrator),
) -> SyncResponseSchema:
    try:
        result = await orchestrator.sync_connection(connection_id)
        return SyncResponseSchema(**result.to_dict())
    except Exception as exc:
        _handle_exception(exc)


@router.delete("/connections/{connection_id}", response_model=DeleteResponseSchema)
async def delete_connection(
    connection_id: str,
    service: IntegrationApplicationService = Depends(get_integration_service),
) -> DeleteResponseSchema:
    try:
        success = await service.delete_connection(connection_id)
        return DeleteResponseSchema(success=success)
    except Exception as exc:
        _handle_exception(exc)