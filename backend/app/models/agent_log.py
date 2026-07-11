"""SQLAlchemy model for agent run logs."""

import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB

from app.core.database import Base


class AgentLog(Base):
    __tablename__ = "agent_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agent_name = Column(String(255), nullable=False)
    run_id = Column(String(255), nullable=False)
    status = Column(String(50), default="running", nullable=False)  # running, completed, failed
    input_data = Column(JSONB, nullable=True, default=dict)
    output_data = Column(JSONB, nullable=True, default=dict)
    error_message = Column(Text, nullable=True)
    duration_ms = Column(JSONB, nullable=True)  # or use Integer
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    def __repr__(self):
        return f"<AgentLog(id={self.id}, agent='{self.agent_name}', status='{self.status}')>"