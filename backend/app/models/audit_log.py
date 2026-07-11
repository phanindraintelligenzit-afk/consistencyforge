"""SQLAlchemy model for audit trail (compliance logging)."""

import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB

from app.core.database import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    action = Column(String(255), nullable=False)  # e.g. consistency_check_run, anomaly_resolved, source_added
    entity_type = Column(String(100), nullable=False)  # e.g. datasource, anomaly, check
    entity_id = Column(String(255), nullable=True)
    actor = Column(String(255), nullable=True)  # user or system agent name
    details = Column(JSONB, nullable=True, default=dict)
    ip_address = Column(String(50), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    def __repr__(self):
        return f"<AuditLog(id={self.id}, action='{self.action}')>"