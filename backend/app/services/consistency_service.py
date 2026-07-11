"""Business logic for consistency checks and anomaly management."""

import uuid
from datetime import datetime, timezone
from typing import Optional, Any

from sqlalchemy import select, func, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.datasource import DataSource
from app.models.consistency_check import ConsistencyCheck
from app.models.anomaly import Anomaly
from app.models.audit_log import AuditLog
from app.schemas.consistency import RunCheckRequest, ResolveAnomalyRequest


class ConsistencyService:
    """Service layer for running consistency checks and managing anomalies."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def run_check(self, req: RunCheckRequest) -> ConsistencyCheck:
        """Execute a consistency check between two data sources."""
        source_a_id = uuid.UUID(req.source_a_id)
        source_b_id = uuid.UUID(req.source_b_id)

        # Verify sources exist
        for sid in [source_a_id, source_b_id]:
            stmt = select(DataSource).where(DataSource.id == sid)
            result = await self.db.execute(stmt)
            if not result.scalar_one_or_none():
                raise ValueError(f"Data source {sid} not found")

        field_mapping_id = uuid.UUID(req.field_mapping_id) if req.field_mapping_id else None

        check = ConsistencyCheck(
            source_a_id=source_a_id,
            source_b_id=source_b_id,
            field_mapping_id=field_mapping_id,
            status="running",
            started_at=datetime.now(timezone.utc),
        )
        self.db.add(check)
        await self.db.flush()
        await self.db.refresh(check)

        # Simulate the check — in production this would invoke agents
        results = {
            "total_fields_compared": 5,
            "matches": 4,
            "mismatches": 1,
            "mismatch_fields": ["revenue_value"],
            "execution_time_ms": 1234,
        }

        check.status = "completed"
        check.results = results
        check.summary = f"Compared 5 fields between sources. Found 4 matches and 1 mismatch."
        check.completed_at = datetime.now(timezone.utc)
        check.updated_at = datetime.now(timezone.utc)

        # Create anomaly for each mismatch
        anomaly = Anomaly(
            check_id=check.id,
            source_a_id=source_a_id,
            source_b_id=source_b_id,
            field_name="revenue_value",
            severity="high",
            status="open",
            source_a_value={"value": 150000},
            source_b_value={"value": 155000},
            expected_value={"value": 150000},
            actual_value={"value": 155000},
        )
        self.db.add(anomaly)

        # Log audit event
        audit_log = AuditLog(
            action="consistency_check_run",
            entity_type="consistency_check",
            entity_id=str(check.id),
            actor="system",
            details={"source_a": str(source_a_id), "source_b": str(source_b_id)},
        )
        self.db.add(audit_log)

        await self.db.flush()
        await self.db.refresh(check)
        return check

    async def list_checks(self, skip: int = 0, limit: int = 50) -> list[ConsistencyCheck]:
        stmt = select(ConsistencyCheck).offset(skip).limit(limit).order_by(ConsistencyCheck.created_at.desc())
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_check(self, check_id: uuid.UUID) -> Optional[ConsistencyCheck]:
        stmt = select(ConsistencyCheck).where(ConsistencyCheck.id == check_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_anomalies(
        self,
        skip: int = 0,
        limit: int = 50,
        severity: Optional[str] = None,
        status: Optional[str] = None,
    ) -> list[Anomaly]:
        stmt = select(Anomaly)
        if severity:
            stmt = stmt.where(Anomaly.severity == severity)
        if status:
            stmt = stmt.where(Anomaly.status == status)
        stmt = stmt.offset(skip).limit(limit).order_by(Anomaly.created_at.desc())
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def resolve_anomaly(self, anomaly_id: uuid.UUID, req: ResolveAnomalyRequest) -> Optional[Anomaly]:
        stmt = select(Anomaly).where(Anomaly.id == anomaly_id)
        result = await self.db.execute(stmt)
        anomaly = result.scalar_one_or_none()
        if not anomaly:
            return None

        anomaly.resolution = req.resolution
        anomaly.status = req.status
        anomaly.updated_at = datetime.now(timezone.utc)

        # Log audit event
        audit_log = AuditLog(
            action="anomaly_resolved",
            entity_type="anomaly",
            entity_id=str(anomaly.id),
            actor="user",
            details={"resolution": req.resolution, "status": req.status},
        )
        self.db.add(audit_log)

        await self.db.flush()
        await self.db.refresh(anomaly)
        return anomaly

    async def get_dashboard_stats(self) -> dict[str, Any]:
        """Aggregate statistics for the dashboard."""
        total_sources = await self.db.execute(select(func.count(DataSource.id)))
        active_sources = await self.db.execute(
            select(func.count(DataSource.id)).where(DataSource.is_active.is_(True))
        )
        total_checks = await self.db.execute(select(func.count(ConsistencyCheck.id)))
        open_anomalies = await self.db.execute(
            select(func.count(Anomaly.id)).where(Anomaly.status == "open")
        )
        resolved_anomalies = await self.db.execute(
            select(func.count(Anomaly.id)).where(Anomaly.status.in_(["resolved", "dismissed"]))
        )
        critical = await self.db.execute(
            select(func.count(Anomaly.id)).where(Anomaly.severity == "critical", Anomaly.status == "open")
        )
        high = await self.db.execute(
            select(func.count(Anomaly.id)).where(Anomaly.severity == "high", Anomaly.status == "open")
        )
        medium = await self.db.execute(
            select(func.count(Anomaly.id)).where(Anomaly.severity == "medium", Anomaly.status == "open")
        )
        low = await self.db.execute(
            select(func.count(Anomaly.id)).where(Anomaly.severity == "low", Anomaly.status == "open")
        )

        return {
            "total_sources": total_sources.scalar() or 0,
            "active_sources": active_sources.scalar() or 0,
            "total_checks": total_checks.scalar() or 0,
            "recent_checks": 0,
            "open_anomalies": open_anomalies.scalar() or 0,
            "resolved_anomalies": resolved_anomalies.scalar() or 0,
            "critical_anomalies": critical.scalar() or 0,
            "high_anomalies": high.scalar() or 0,
            "medium_anomalies": medium.scalar() or 0,
            "low_anomalies": low.scalar() or 0,
        }