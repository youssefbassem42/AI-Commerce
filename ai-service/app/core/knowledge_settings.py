from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class KnowledgeSettings(BaseSettings):
    """Knowledge Base module settings."""

    documents_collection: str = "knowledge_documents"
    chunks_collection: str = "knowledge_chunks"
    summaries_collection: str = "knowledge_business_summaries"
    route_prefix: str = "/api/v1/knowledge-base"
    default_page_size: int = 20
    max_page_size: int = 100

    model_config = SettingsConfigDict(
        env_prefix="KNOWLEDGE_",
        env_file=".env",
        extra="ignore",
    )


@lru_cache
def get_knowledge_settings() -> KnowledgeSettings:
    return KnowledgeSettings()


knowledge_settings = get_knowledge_settings()
