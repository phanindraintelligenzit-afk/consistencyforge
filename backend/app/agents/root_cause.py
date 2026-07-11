"""RootCauseAgent — LangGraph agent that analyzes root cause of anomalies."""

from typing import Any, TypedDict, Optional

from langgraph.graph import StateGraph, END


class RootCauseState(TypedDict):
    """State for root cause analysis."""
    anomaly_id: str
    field_name: str
    source_a_value: Any
    source_b_value: Any
    source_a_type: str
    source_b_type: str
    analysis: Optional[str]
    root_cause: Optional[str]
    confidence: float
    error: Optional[str]


def classify_mismatch(state: RootCauseState) -> dict[str, Any]:
    """Classify the type of mismatch."""
    a_val = state.get("source_a_value")
    b_val = state.get("source_b_value")

    if a_val is None and b_val is not None:
        return {"mismatch_type": "missing_in_source_a"}
    elif a_val is not None and b_val is None:
        return {"mismatch_type": "missing_in_source_b"}
    elif a_val != b_val:
        # Check if it's a rounding difference
        try:
            if isinstance(a_val, (int, float)) and isinstance(b_val, (int, float)):
                diff_pct = abs(a_val - b_val) / max(abs(a_val), abs(b_val), 1)
                if diff_pct < 0.05:
                    return {"mismatch_type": "rounding_difference"}
                else:
                    return {"mismatch_type": "value_mismatch"}
            if isinstance(a_val, str) and isinstance(b_val, str):
                if a_val.lower() == b_val.lower():
                    return {"mismatch_type": "case_difference"}
                return {"mismatch_type": "string_mismatch"}
            return {"mismatch_type": "value_mismatch"}
        except (TypeError, ValueError):
            return {"mismatch_type": "value_mismatch"}
    return {"mismatch_type": "unknown"}


def analyze_root_cause(state: RootCauseState) -> dict[str, Any]:
    """Analyze the root cause of the anomaly."""
    mismatch_type = state.get("mismatch_type", "unknown")
    field = state.get("field_name", "unknown")

    root_causes = {
        "missing_in_source_a": f"Record exists in source B but not in source A for field '{field}'. Likely a delayed sync or partial data export.",
        "missing_in_source_b": f"Record exists in source A but not in source B for field '{field}'. Likely an incomplete import or filtering issue.",
        "rounding_difference": f"Values for '{field}' differ slightly (within 5%). Likely a rounding/precision difference between systems.",
        "case_difference": f"String values for '{field}' differ only in casing. Likely a case-sensitivity configuration mismatch.",
        "string_mismatch": f"String values for '{field}' are different. Could be due to timestamp formatting, encoding, or data entry differences.",
        "value_mismatch": f"Values for '{field}' are substantially different. Possible data corruption, stale data, or business logic discrepancy.",
        "unknown": f"Cannot determine the root cause for '{field}'. Manual investigation required.",
    }

    root_cause = root_causes.get(mismatch_type, root_causes["unknown"])
    confidence = 0.4 if mismatch_type == "unknown" else 0.75

    return {
        "root_cause": root_cause,
        "confidence": confidence,
        "analysis": f"Anomaly in field '{field}': {mismatch_type}. {root_cause}",
        "error": None,
    }


# Build the LangGraph
workflow = StateGraph(RootCauseState)
workflow.add_node("classify_mismatch", classify_mismatch)
workflow.add_node("analyze_root_cause", analyze_root_cause)

workflow.set_entry_point("classify_mismatch")
workflow.add_edge("classify_mismatch", "analyze_root_cause")
workflow.add_edge("analyze_root_cause", END)

root_cause_agent = workflow.compile()


async def run_root_cause_analysis(
    anomaly_id: str,
    field_name: str,
    source_a_value: Any,
    source_b_value: Any,
    source_a_type: str = "postgresql",
    source_b_type: str = "postgresql",
) -> dict[str, Any]:
    """Run the root cause analysis agent."""
    initial_state: RootCauseState = {
        "anomaly_id": anomaly_id,
        "field_name": field_name,
        "source_a_value": source_a_value,
        "source_b_value": source_b_value,
        "source_a_type": source_a_type,
        "source_b_type": source_b_type,
        "analysis": None,
        "root_cause": None,
        "confidence": 0.0,
        "error": None,
    }
    result = await root_cause_agent.ainvoke(initial_state)
    return result