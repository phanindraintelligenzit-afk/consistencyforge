"""ReconciliationOrchestratorAgent — LangGraph agent that orchestrates reconciliation."""

from typing import Any, TypedDict, Optional

from langgraph.graph import StateGraph, END


class ReconciliationState(TypedDict):
    """State for reconciliation orchestration."""
    check_id: str
    source_a_id: str
    source_b_id: str
    anomalies: list[dict[str, Any]]
    field_mappings: dict[str, str]
    root_causes: Optional[dict[str, str]]
    proposed_fixes: Optional[list[dict[str, Any]]]
    reconciliation_plan: Optional[dict[str, Any]]
    status: str
    error: Optional[str]


def gather_anomaly_details(state: ReconciliationState) -> dict[str, Any]:
    """Collect all anomalies and group by severity."""
    anomalies = state.get("anomalies", [])

    grouped = {
        "critical": [a for a in anomalies if a.get("severity") == "critical"],
        "high": [a for a in anomalies if a.get("severity") == "high"],
        "medium": [a for a in anomalies if a.get("severity") == "medium"],
        "low": [a for a in anomalies if a.get("severity") == "low"],
    }

    root_causes = {}
    for a in anomalies:
        root_causes[a.get("field_name", "unknown")] = a.get("root_cause", "unknown")

    return {
        "grouped_anomalies": grouped,
        "root_causes": root_causes,
    }


def create_reconciliation_plan(state: ReconciliationState) -> dict[str, Any]:
    """Create a reconciliation plan based on anomaly severity and root causes."""
    grouped = state.get("grouped_anomalies", {})
    root_causes = state.get("root_causes", {})

    plan = {
        "check_id": state["check_id"],
        "total_anomalies": len(state.get("anomalies", [])),
        "priority_order": [],
        "steps": [],
        "estimated_fix_time_minutes": 0,
        "auto_fix_count": 0,
        "manual_fix_count": 0,
    }

    # Process critical and high first
    for severity in ["critical", "high", "medium", "low"]:
        for anomaly in grouped.get(severity, []):
            field = anomaly.get("field_name", "unknown")
            root_cause = root_causes.get(field, "unknown")
            needs_manual = "manually" in root_cause.lower() or "corruption" in root_cause.lower()

            step = {
                "field_name": field,
                "severity": severity,
                "root_cause": root_cause,
                "fix_type": "manual" if needs_manual else "auto",
                "source_a_value": anomaly.get("source_a_value"),
                "source_b_value": anomaly.get("source_b_value"),
            }

            plan["steps"].append(step)
            plan["priority_order"].append(field)

            if needs_manual:
                plan["manual_fix_count"] += 1
                plan["estimated_fix_time_minutes"] += 10
            else:
                plan["auto_fix_count"] += 1
                plan["estimated_fix_time_minutes"] += 2

    return {
        "reconciliation_plan": plan,
        "status": "planned",
        "error": None,
    }


# Build the LangGraph
workflow = StateGraph(ReconciliationState)
workflow.add_node("gather_anomaly_details", gather_anomaly_details)
workflow.add_node("create_reconciliation_plan", create_reconciliation_plan)

workflow.set_entry_point("gather_anomaly_details")
workflow.add_edge("gather_anomaly_details", "create_reconciliation_plan")
workflow.add_edge("create_reconciliation_plan", END)

reconciliation_orchestrator = workflow.compile()


async def run_reconciliation(
    check_id: str,
    source_a_id: str,
    source_b_id: str,
    anomalies: list[dict[str, Any]],
    field_mappings: dict[str, str],
) -> dict[str, Any]:
    """Run the reconciliation orchestrator."""
    initial_state: ReconciliationState = {
        "check_id": check_id,
        "source_a_id": source_a_id,
        "source_b_id": source_b_id,
        "anomalies": anomalies,
        "field_mappings": field_mappings,
        "root_causes": None,
        "proposed_fixes": None,
        "reconciliation_plan": None,
        "status": "gathering",
        "error": None,
    }
    result = await reconciliation_orchestrator.ainvoke(initial_state)
    return result