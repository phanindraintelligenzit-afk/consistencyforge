"""SQLAlchemy model for field mappings between data sources."""

import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, Float, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB

from app.core.database import Base


class FieldMapping(Base):
    __tablename__ = "field_mappings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_a_id = Column(UUID(as_uuid=True), ForeignKey("data_sources.id", ondelete="CASCADE"), nullable=False)
    source_b_id = Column(UUID(as_uuid=True), ForeignKey("data_sources.id", ondelete="CASCADE"), nullable=False)
    fields = Column(JSONB, nullable=False, default=dict)  # {"source_a_field": "source_b_field", ...}
    confidence = Column(Float, default=1.0, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc),
                        onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    def __repr__(self):
        return f"<FieldMapping(id={self.id}, src_a={self.source_a_id}, src_b={self.source_b_id})>"