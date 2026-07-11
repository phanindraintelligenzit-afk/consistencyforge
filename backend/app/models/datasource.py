"""SQLAlchemy model for the data_sources table."""

import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, String, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB

from app.core.database import Base


class DataSource(Base):
    __tablename__ = "data_sources"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False, unique=True)
    source_type = Column(String(100), nullable=False)  # e.g. postgresql, mysql, csv, api, mongodb
    connection_config = Column(JSONB, nullable=False, default=dict)
    schema_snapshot = Column(JSONB, nullable=True, default=dict)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc),
                        onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    def __repr__(self):
        return f"<DataSource(id={self.id}, name='{self.name}', type='{self.source_type}')>"