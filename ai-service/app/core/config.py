import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application settings using pydantic-settings."""
    PROJECT_NAME: str = "AI Commerce Platform"
    
    MONGO_URI: str = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    MONGO_DB: str = os.getenv("MONGO_DB", "ai_commerce")
    
    QDRANT_URL: str = os.getenv("QDRANT_URL", "http://localhost:6333")
    
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
