"""Business logic for data source management."""

import uuid
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.datasource import DataSource
from app.schemas.source import DataSourceCreate


class SourceService:
    """Service layer for data source CRUD and sync operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_sources(self, skip: int = 0, limit: int = 100) -> list[DataSource]:
        stmt = select(DataSource).offset(skip).limit(limit).order_by(DataSource.created_at.desc())
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_source(self, source_id: uuid.UUID) -> Optional[DataSource]:
        stmt = select(DataSource).where(DataSource.id == source_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create_source(self, data: DataSourceCreate) -> DataSource:
        # Check for duplicate name
        stmt = select(DataSource).where(DataSource.name == data.name)
        result = await self.db.execute(stmt)
        if result.scalar_one_or_none():
            raise ValueError(f"Data source with name '{data.name}' already exists")

        source = DataSource(
            name=data.name,
            source_type=data.source_type,
            connection_config=data.connection_config or {},
            schema_snapshot=data.schema_snapshot or {},
            is_active=data.is_active,
        )
        self.db.add(source)
        await self.db.flush()
        await self.db.refresh(source)
        return source

    async def delete_source(self, source_id: uuid.UUID) -> bool:
        stmt = select(DataSource).where(DataSource.id == source_id)
        result = await self.db.execute(stmt)
        source = result.scalar_one_or_none()
        if not source:
            return False
        await self.db.delete(source)
        await self.db.flush()
        return True

    async def sync_source(self, source_id: uuid.UUID) -> Optional[DataSource]:
        """Simulate syncing schema from a data source."""
        source = await self.get_source(source_id)
        if not source:
            return None

        # In production, this would connect to the actual source and introspect schema
        source.schema_snapshot = {
            "tables": [
                {
                    "name": "sample_table",
                    "columns": [
                        {"name": "id", "type": "integer", "nullable": False},
                        {"name": "name", "type": "varchar(255)", "nullable": False},
                        {"name": "value", "type": "decimal", "nullable": True},
                        {"name": "created_at", "type": "timestamp", "nullable": False},
                    ],
                }
            ],
            "synced_at": datetime.now(timezone.utc).isoformat(),
        }
        source.updated_at = datetime.now(timezone.utc)
        await self.db.flush()
        await self.db.refresh(source)
        return source