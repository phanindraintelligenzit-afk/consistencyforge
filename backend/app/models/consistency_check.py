"""SQLAlchemy model for consistency checks."""

import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, String, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB

from app.core.database import Base


class ConsistencyCheck(Base):
    __tablename__ = "consistency_checks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_a_id = Column(UUID(as_uuid=True), ForeignKey("data_sources.id", ondelete="CASCADE"), nullable=False)
    source_b_id = Column(UUID(as_uuid=True), ForeignKey("data_sources.id", ondelete="CASCADE"), nullable=False)
    field_mapping_id = Column(UUID(as_uuid=True), ForeignKey("field_mappings.id", ondelete="SET NULL"), nullable=True)
    status = Column(String(50), default="pending", nullable=False)  # pending, running, completed, failed
    results = Column(JSONB, nullable=True, default=dict)
    summary = Column(Text, nullable=True)
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc),
                        onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    def __repr__(self):
        return f"<ConsistencyCheck(id={self.id}, status='{self.status}')>"