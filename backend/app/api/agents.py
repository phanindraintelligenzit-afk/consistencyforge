"""Agent status API endpoint."""

from fastapi import APIRouter
from typing import Any

router = APIRouter(prefix="/api/agents", tags=["agents"])

AGENTS = [
    {"name": "SchemaIngestionAgent", "description": "Parses schema definitions from data source configs", "status": "idle"},
    {"name": "FieldMapperAgent", "description": "Maps semantically equivalent fields using LLM", "status": "idle"},
    {"name": "ConsistencyScannerAgent", "description": "Cross-system value comparison", "status": "idle"},
    {"name": "RootCauseAgent", "description": "Analyzes root cause of anomalies", "status": "idle"},
    {"name": "AutoHealAgent", "description": "Proposes fixes for anomalies", "status": "idle"},
    {"name": "ReconciliationOrchestratorAgent", "description": "Orchestrates reconciliation", "status": "idle"},
    {"name": "AuditTrailAgent", "description": "Logging/compliance agent", "status": "idle"},
]


@router.get("/")
async def list_agents() -> dict[str, list[dict[str, Any]]]:
    """List all available agents and their statuses."""
    return {"agents": AGENTS}


@router.get("/{agent_name}")
async def get_agent(agent_name: str) -> dict[str, Any]:
    """Get status for a specific agent."""
    for agent in AGENTS:
        if agent["name"] == agent_name:
            return agent
    return {"error": f"Agent '{agent_name}' not found", "status": "unknown"}