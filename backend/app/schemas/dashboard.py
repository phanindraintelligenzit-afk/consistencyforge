"""Pydantic schemas for dashboard summary."""

from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime
import uuid


class DashboardStats(BaseModel):
    total_sources: int
    active_sources: int
    total_checks: int
    recent_checks: int
    open_anomalies: int
    resolved_anomalies: int
    critical_anomalies: int
    high_anomalies: int
    medium_anomalies: int
    low_anomalies: int


class AnomalyTrendPoint(BaseModel):
    date: str
    count: int
    severity: str


class RecentActivityItem(BaseModel):
    id: uuid.UUID
    action: str
    entity_type: str
    actor: Optional[str] = None
    details: Optional[Any] = None
    created_at: datetime


class DashboardResponse(BaseModel):
    stats: DashboardStats
    anomaly_trend: list[AnomalyTrendPoint]
    recent_activity: list[RecentActivityItem]