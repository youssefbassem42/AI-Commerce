from celery import Celery

from app.core.config import settings

celery_app = Celery(
    "ai_commerce_tasks",
    broker=settings.REDIS_SETTINGS.REDIS_URL,
    backend=settings.REDIS_SETTINGS.REDIS_URL,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    imports=["app.infrastructure.tasks.celery_tasks"],
)
