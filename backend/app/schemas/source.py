"""Pydantic schemas for data sources."""

from pydantic import BaseModel, Field
from typing import Optional, Any
from datetime import datetime
import uuid


class DataSourceCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    source_type: str = Field(..., description="Type of data source: postgresql, mysql, csv, api, mongodb")
    connection_config: dict[str, Any] = Field(default_factory=dict)
    schema_snapshot: Optional[dict[str, Any]] = None
    is_active: bool = True


class DataSourceUpdate(BaseModel):
    name: Optional[str] = None
    connection_config: Optional[dict[str, Any]] = None
    schema_snapshot: Optional[dict[str, Any]] = None
    is_active: Optional[bool] = None


class DataSourceResponse(BaseModel):
    id: uuid.UUID
    name: str
    source_type: str
    connection_config: dict[str, Any]
    schema_snapshot: Optional[dict[str, Any]] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class DataSourceListResponse(BaseModel):
    items: list[DataSourceResponse]
    total: int