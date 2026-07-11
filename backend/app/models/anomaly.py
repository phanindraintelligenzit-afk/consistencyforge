"""SQLAlchemy model for anomalies detected during consistency checks."""

import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, String, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB

from app.core.database import Base


class Anomaly(Base):
    __tablename__ = "anomalies"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    check_id = Column(UUID(as_uuid=True), ForeignKey("consistency_checks.id", ondelete="CASCADE"), nullable=False)
    source_a_id = Column(UUID(as_uuid=True), ForeignKey("data_sources.id", ondelete="CASCADE"), nullable=False)
    source_b_id = Column(UUID(as_uuid=True), ForeignKey("data_sources.id", ondelete="CASCADE"), nullable=False)
    field_name = Column(String(255), nullable=False)
    severity = Column(String(50), default="medium", nullable=False)  # low, medium, high, critical
    status = Column(String(50), default="open", nullable=False)  # open, investigating, resolved, dismissed
    source_a_value = Column(JSONB, nullable=True)
    source_b_value = Column(JSONB, nullable=True)
    expected_value = Column(JSONB, nullable=True)
    actual_value = Column(JSONB, nullable=True)
    root_cause = Column(Text, nullable=True)
    resolution = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc),
                        onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    def __repr__(self):
        return f"<Anomaly(id={self.id}, field='{self.field_name}', severity='{self.severity}')>"