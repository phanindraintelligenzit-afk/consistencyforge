"""AuditTrailAgent — LangGraph agent for logging/compliance."""

from typing import Any, TypedDict, Optional
from datetime import datetime, timezone

from langgraph.graph import StateGraph, END


class AuditTrailState(TypedDict):
    """State for audit trail logging."""
    action: str
    entity_type: str
    entity_id: str
    actor: str
    details: dict[str, Any]
    ip_address: Optional[str]
    compliance_tags: Optional[list[str]]
    log_entry: Optional[dict[str, Any]]
    log_status: str
    error: Optional[str]


def verify_compliance(state: AuditTrailState) -> dict[str, Any]:
    """Check compliance requirements for the audit event."""
    action = state.get("action", "")
    entity_type = state.get("entity_type", "")

    tags = ["audit"]
    if "anomaly" in action.lower() or "anomaly" in entity_type.lower():
        tags.append("data_quality")
    if "source" in action.lower() or "datasource" in entity_type.lower():
        tags.append("data_governance")
    if "check" in action.lower() or "consistency" in entity_type.lower():
        tags.append("monitoring")
    if "resolve" in action.lower():
        tags.append("remediation")

    return {"compliance_tags": tags}


def build_log_entry(state: AuditTrailState) -> dict[str, Any]:
    """Build and persist the audit log entry."""
    now = datetime.now(timezone.utc)

    log_entry = {
        "action": state["action"],
        "entity_type": state["entity_type"],
        "entity_id": state["entity_id"],
        "actor": state["actor"],
        "details": state.get("details", {}),
        "ip_address": state.get("ip_address"),
        "compliance_tags": state.get("compliance_tags", ["audit"]),
        "timestamp": now.isoformat(),
        "version": "1.0",
        "status": "recorded",
    }

    return {
        "log_entry": log_entry,
        "log_status": "recorded",
        "error": None,
    }


# Build the LangGraph
workflow = StateGraph(AuditTrailState)
workflow.add_node("verify_compliance", verify_compliance)
workflow.add_node("build_log_entry", build_log_entry)

workflow.set_entry_point("verify_compliance")
workflow.add_edge("verify_compliance", "build_log_entry")
workflow.add_edge("build_log_entry", END)

audit_trail_agent = workflow.compile()


async def run_audit_logging(
    action: str,
    entity_type: str,
    entity_id: str,
    actor: str = "system",
    details: Optional[dict[str, Any]] = None,
    ip_address: Optional[str] = None,
) -> dict[str, Any]:
    """Run the audit trail agent."""
    initial_state: AuditTrailState = {
        "action": action,
        "entity_type": entity_type,
        "entity_id": entity_id,
        "actor": actor,
        "details": details or {},
        "ip_address": ip_address,
        "compliance_tags": None,
        "log_entry": None,
        "log_status": "pending",
        "error": None,
    }
    result = await audit_trail_agent.ainvoke(initial_state)
    return result