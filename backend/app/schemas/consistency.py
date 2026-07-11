"""Pydantic schemas for consistency checks and anomalies."""

from pydantic import BaseModel, Field
from typing import Optional, Any
from datetime import datetime
import uuid


class RunCheckRequest(BaseModel):
    source_a_id: str = Field(..., description="UUID of the first data source")
    source_b_id: str = Field(..., description="UUID of the second data source")
    field_mapping_id: Optional[str] = None


class ConsistencyCheckResponse(BaseModel):
    id: uuid.UUID
    source_a_id: uuid.UUID
    source_b_id: uuid.UUID
    field_mapping_id: Optional[uuid.UUID] = None
    status: str
    results: Optional[dict[str, Any]] = None
    summary: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ConsistencyCheckListResponse(BaseModel):
    items: list[ConsistencyCheckResponse]
    total: int


class AnomalyResponse(BaseModel):
    id: uuid.UUID
    check_id: uuid.UUID
    source_a_id: uuid.UUID
    source_b_id: uuid.UUID
    field_name: str
    severity: str
    status: str
    source_a_value: Optional[Any] = None
    source_b_value: Optional[Any] = None
    expected_value: Optional[Any] = None
    actual_value: Optional[Any] = None
    root_cause: Optional[str] = None
    resolution: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class AnomalyListResponse(BaseModel):
    items: list[AnomalyResponse]
    total: int


class ResolveAnomalyRequest(BaseModel):
    resolution: str = Field(..., min_length=1)
    status: str = Field(default="resolved", pattern="^(resolved|dismissed)$")