"""Sources API router — CRUD for data sources."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
import uuid

from app.core.database import get_db
from app.models.datasource import DataSource
from app.schemas.source import DataSourceCreate, DataSourceUpdate, DataSourceResponse, DataSourceListResponse
from app.services.source_service import SourceService

router = APIRouter(prefix="/api/sources", tags=["sources"])


def _get_source_service(db: AsyncSession = Depends(get_db)) -> SourceService:
    return SourceService(db)


@router.get("/", response_model=DataSourceListResponse)
async def list_sources(
    skip: int = 0,
    limit: int = 100,
    service: SourceService = Depends(_get_source_service),
):
    """List all data sources."""
    items = await service.list_sources(skip=skip, limit=limit)
    return DataSourceListResponse(items=items, total=len(items))


@router.post("/", response_model=DataSourceResponse, status_code=status.HTTP_201_CREATED)
async def create_source(
    data: DataSourceCreate,
    service: SourceService = Depends(_get_source_service),
):
    """Create a new data source."""
    try:
        return await service.create_source(data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{source_id}", response_model=DataSourceResponse)
async def get_source(
    source_id: uuid.UUID,
    service: SourceService = Depends(_get_source_service),
):
    """Get a data source by ID."""
    source = await service.get_source(source_id)
    if not source:
        raise HTTPException(status_code=404, detail="Data source not found")
    return source


@router.delete("/{source_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_source(
    source_id: uuid.UUID,
    service: SourceService = Depends(_get_source_service),
):
    """Delete a data source."""
    deleted = await service.delete_source(source_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Data source not found")
    return None


@router.post("/{source_id}/sync", response_model=DataSourceResponse)
async def sync_source(
    source_id: uuid.UUID,
    service: SourceService = Depends(_get_source_service),
):
    """Trigger a schema sync for a data source."""
    source = await service.sync_source(source_id)
    if not source:
        raise HTTPException(status_code=404, detail="Data source not found")
    return source