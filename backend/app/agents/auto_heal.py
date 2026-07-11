"""AutoHealAgent — LangGraph agent that proposes fixes for anomalies."""

from typing import Any, TypedDict, Optional

from langgraph.graph import StateGraph, END


class AutoHealState(TypedDict):
    """State for auto-heal proposals."""
    anomaly_id: str
    field_name: str
    root_cause: str
    source_a_value: Any
    source_b_value: Any
    source_a_is_authoritative: bool
    proposed_fix: Optional[str]
    fix_confidence: float
    requires_approval: bool
    error: Optional[str]


def evaluate_authority(state: AutoHealState) -> dict[str, Any]:
    """Determine which source is authoritative and if auto-fix is safe."""
    is_auth = state.get("source_a_is_authoritative", False)
    root_cause = state.get("root_cause", "")

    # Determine if the fix requires manual approval
    needs_approval = True
    if "rounding" in root_cause.lower():
        needs_approval = False
    elif "case" in root_cause.lower():
        needs_approval = False

    return {
        "source_a_is_authoritative": is_auth,
        "requires_approval": needs_approval,
    }


def propose_fix(state: AutoHealState) -> dict[str, Any]:
    """Propose a fix for the anomaly."""
    field = state.get("field_name", "unknown")
    is_auth = state.get("source_a_is_authoritative", False)
    a_val = state.get("source_a_value")
    b_val = state.get("source_b_value")
    root_cause = state.get("root_cause", "")

    if is_auth:
        # Source A is authoritative, propose updating source B
        proposed_fix = f"Update '{field}' in source B from '{b_val}' to '{a_val}' (using source A as authoritative reference)"
        fix_confidence = 0.9
    else:
        # Source B is authoritative
        proposed_fix = f"Update '{field}' in source A from '{a_val}' to '{b_val}' (using source B as authoritative reference)"
        fix_confidence = 0.9

    if "rounding" in root_cause.lower():
        recommended = a_val if is_auth else b_val
        proposed_fix = f"Align precision for '{field}'. Standardize to value '{recommended}' across both systems."
        fix_confidence = 0.95

    if "case" in root_cause.lower():
        proposed_fix = f"Normalize casing for '{field}'. Apply consistent formatting: lowercased values across both systems."
        fix_confidence = 0.95

    return {
        "proposed_fix": proposed_fix,
        "fix_confidence": fix_confidence,
        "error": None,
    }


# Build the LangGraph
workflow = StateGraph(AutoHealState)
workflow.add_node("evaluate_authority", evaluate_authority)
workflow.add_node("propose_fix", propose_fix)

workflow.set_entry_point("evaluate_authority")
workflow.add_edge("evaluate_authority", "propose_fix")
workflow.add_edge("propose_fix", END)

auto_heal_agent = workflow.compile()


async def run_auto_heal(
    anomaly_id: str,
    field_name: str,
    root_cause: str,
    source_a_value: Any,
    source_b_value: Any,
    source_a_is_authoritative: bool = True,
) -> dict[str, Any]:
    """Run the auto-heal agent."""
    initial_state: AutoHealState = {
        "anomaly_id": anomaly_id,
        "field_name": field_name,
        "root_cause": root_cause,
        "source_a_value": source_a_value,
        "source_b_value": source_b_value,
        "source_a_is_authoritative": source_a_is_authoritative,
        "proposed_fix": None,
        "fix_confidence": 0.0,
        "requires_approval": True,
        "error": None,
    }
    result = await auto_heal_agent.ainvoke(initial_state)
    return result