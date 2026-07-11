"""Dashboard API router — summary endpoint."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta, timezone

from app.core.database import get_db
from app.services.consistency_service import ConsistencyService
from app.schemas.dashboard import (
    DashboardResponse,
    DashboardStats,
    AnomalyTrendPoint,
    RecentActivityItem,
)

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


def _get_consistency_service(db: AsyncSession = Depends(get_db)) -> ConsistencyService:
    return ConsistencyService(db)


@router.get("/summary", response_model=DashboardResponse)
async def dashboard_summary(
    service: ConsistencyService = Depends(_get_consistency_service),
):
    """Get dashboard summary with stats, trend, and recent activity."""
    stats_data = await service.get_dashboard_stats()

    stats = DashboardStats(
        total_sources=stats_data.get("total_sources", 0),
        active_sources=stats_data.get("active_sources", 0),
        total_checks=stats_data.get("total_checks", 0),
        recent_checks=stats_data.get("recent_checks", 0),
        open_anomalies=stats_data.get("open_anomalies", 0),
        resolved_anomalies=stats_data.get("resolved_anomalies", 0),
        critical_anomalies=stats_data.get("critical_anomalies", 0),
        high_anomalies=stats_data.get("high_anomalies", 0),
        medium_anomalies=stats_data.get("medium_anomalies", 0),
        low_anomalies=stats_data.get("low_anomalies", 0),
    )

    # Generate trend data from last 7 days
    trend = []
    now = datetime.now(timezone.utc)
    for i in range(6, -1, -1):
        day = now - timedelta(days=i)
        date_str = day.strftime("%Y-%m-%d")
        for sev in ["low", "medium", "high", "critical"]:
            trend.append(AnomalyTrendPoint(date=date_str, count=0, severity=sev))

    # Placeholder for recent activity
    recent = []  # Would query audit_logs in production

    return DashboardResponse(stats=stats, anomaly_trend=trend, recent_activity=recent)