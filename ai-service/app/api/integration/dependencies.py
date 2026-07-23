from fastapi import Depends

from app.application.integration.mapping.services import IntegrationApplicationService
from app.application.integration.sync.orchestrator import SyncOrchestrator
from app.infrastructure.mongodb.repositories.integration_connection_repository import (
    IntegrationConnectionMongoRepository,
)
from app.infrastructure.security.key_manager import KeyManager


def get_integration_connection_repository() -> IntegrationConnectionMongoRepository:
    return IntegrationConnectionMongoRepository()


def get_key_manager() -> KeyManager:
    return KeyManager()


def get_integration_service(
    repository: IntegrationConnectionMongoRepository = Depends(get_integration_connection_repository),
    key_manager: KeyManager = Depends(get_key_manager),
) -> IntegrationApplicationService:
    return IntegrationApplicationService(
        repository=repository,
        key_manager=key_manager,
    )


def get_sync_orchestrator(
    repository: IntegrationConnectionMongoRepository = Depends(get_integration_connection_repository),
    key_manager: KeyManager = Depends(get_key_manager),
) -> SyncOrchestrator:
    return SyncOrchestrator(
        repository=repository,
        key_manager=key_manager,
    )