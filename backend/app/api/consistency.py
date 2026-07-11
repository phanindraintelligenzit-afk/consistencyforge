"""Consistency API router — run checks, list anomalies, resolve anomalies."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
import uuid

from app.core.database import get_db
from app.services.consistency_service import ConsistencyService
from app.schemas.consistency import (
    RunCheckRequest,
    ConsistencyCheckResponse,
    ConsistencyCheckListResponse,
    AnomalyResponse,
    AnomalyListResponse,
    ResolveAnomalyRequest,
)

router = APIRouter(prefix="/api/consistency", tags=["consistency"])


def _get_consistency_service(db: AsyncSession = Depends(get_db)) -> ConsistencyService:
    return ConsistencyService(db)


@router.post("/checks", response_model=ConsistencyCheckResponse, status_code=status.HTTP_201_CREATED)
async def run_consistency_check(
    req: RunCheckRequest,
    service: ConsistencyService = Depends(_get_consistency_service),
):
    """Run a consistency check between two data sources."""
    try:
        return await service.run_check(req)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/checks", response_model=ConsistencyCheckListResponse)
async def list_checks(
    skip: int = 0,
    limit: int = 50,
    service: ConsistencyService = Depends(_get_consistency_service),
):
    """List all consistency checks."""
    items = await service.list_checks(skip=skip, limit=limit)
    return ConsistencyCheckListResponse(items=items, total=len(items))


@router.get("/checks/{check_id}", response_model=ConsistencyCheckResponse)
async def get_check(
    check_id: uuid.UUID,
    service: ConsistencyService = Depends(_get_consistency_service),
):
    """Get a specific consistency check."""
    check = await service.get_check(check_id)
    if not check:
        raise HTTPException(status_code=404, detail="Consistency check not found")
    return check


@router.get("/anomalies", response_model=AnomalyListResponse)
async def list_anomalies(
    skip: int = 0,
    limit: int = 50,
    severity: Optional[str] = None,
    status: Optional[str] = None,
    service: ConsistencyService = Depends(_get_consistency_service),
):
    """List anomalies with optional filters."""
    items = await service.list_anomalies(skip=skip, limit=limit, severity=severity, status=status)
    return AnomalyListResponse(items=items, total=len(items))


@router.put("/anomalies/{anomaly_id}/resolve", response_model=AnomalyResponse)
async def resolve_anomaly(
    anomaly_id: uuid.UUID,
    req: ResolveAnomalyRequest,
    service: ConsistencyService = Depends(_get_consistency_service),
):
    """Resolve or dismiss an anomaly."""
    anomaly = await service.resolve_anomaly(anomaly_id, req)
    if not anomaly:
        raise HTTPException(status_code=404, detail="Anomaly not found")
    return anomaly