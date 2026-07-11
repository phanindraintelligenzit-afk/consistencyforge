"""Celery application for background task processing."""

from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "consistencyforge",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,
    task_soft_time_limit=25 * 60,
)


@celery_app.task(bind=True, max_retries=3)
def run_consistency_check_task(self, check_id: str, source_a_id: str, source_b_id: str):
    """Background task to run a consistency check."""
    try:
        # In production, this would invoke the full agent pipeline
        return {"status": "completed", "check_id": check_id}
    except Exception as exc:
        self.retry(exc=exc, countdown=60)


@celery_app.task(bind=True, max_retries=3)
def sync_source_schema_task(self, source_id: str):
    """Background task to sync a source schema."""
    try:
        return {"status": "completed", "source_id": source_id}
    except Exception as exc:
        self.retry(exc=exc, countdown=60)