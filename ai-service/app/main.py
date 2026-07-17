from fastapi import FastAPI

from app.api.ai.router import router as ai_router
from app.api.chat.router import router as chat_router
from app.api.knowledge.generation_router import router as knowledge_generation_router
from app.api.knowledge.retrieval_router import router as knowledge_retrieval_router
from app.api.knowledge.job_router import router as knowledge_job_router
from app.api.knowledge.unified_router import router as knowledge_unified_router
from app.api.rag.router import router as rag_router
from app.core.config import settings
from app.middleware.logging import AITracingMiddleware
from app.middleware.rate_limit import RateLimitMiddleware

app = FastAPI(title=settings.PROJECT_NAME)

app.add_middleware(RateLimitMiddleware, limit_per_minute=100)
app.add_middleware(AITracingMiddleware)

app.include_router(chat_router)
app.include_router(ai_router)
app.include_router(knowledge_generation_router)
app.include_router(knowledge_retrieval_router)
app.include_router(knowledge_job_router)
app.include_router(knowledge_unified_router)
app.include_router(rag_router)


@app.get("/health/")
def health_check():
    return {"status": "AI Service is live !"}
