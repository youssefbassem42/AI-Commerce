from fastapi import FastAPI

from app.api.ai.router import router as ai_router
from app.api.chat.router import router as chat_router
from app.core.config import settings
from app.middleware.logging import AITracingMiddleware
from app.middleware.rate_limit import RateLimitMiddleware

app = FastAPI(title=settings.PROJECT_NAME)

app.add_middleware(RateLimitMiddleware, limit_per_minute=100)
app.add_middleware(AITracingMiddleware)

app.include_router(chat_router)
app.include_router(ai_router)


@app.get("/health/")
def health_check():
    return {"status": "AI Service is live !"}
