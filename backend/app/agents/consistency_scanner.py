"""ConsistencyScannerAgent — LangGraph agent for cross-system value comparison."""

from typing import Any, TypedDict, Optional
import random

from langgraph.graph import StateGraph, END


class ScannerState(TypedDict):
    """State for consistency scanning."""
    source_a_id: str
    source_b_id: str
    field_mappings: dict[str, str]
    source_a_data: Optional[list[dict[str, Any]]]
    source_b_data: Optional[list[dict[str, Any]]]
    comparison_results: Optional[dict[str, Any]]
    anomalies: list[dict[str, Any]]
    error: Optional[str]


def fetch_source_data(state: ScannerState) -> dict[str, Any]:
    """Simulate fetching sample data from both sources."""
    # In production, this would query actual databases/APIs
    source_a_data = [
        {"id": 1, "email": "alice@example.com", "name": "Alice", "amount": 100.0},
        {"id": 2, "email": "bob@example.com", "name": "Bob", "amount": 250.0},
        {"id": 3, "email": "charlie@example.com", "name": "Charlie", "amount": 150.0},
    ]
    source_b_data = [
        {"id": 1, "email_address": "alice@example.com", "full_name": "Alice", "value": 100.0},
        {"id": 2, "email_address": "bob@example.com", "full_name": "Bob Smith", "value": 260.0},
        {"id": 3, "email_address": "charlie@example.com", "full_name": "Charlie", "value": 150.0},
    ]
    return {"source_a_data": source_a_data, "source_b_data": source_b_data}


def compare_values(state: ScannerState) -> dict[str, Any]:
    """Compare values between sources using field mappings."""
    mappings = state.get("field_mappings", {})
    data_a = state.get("source_a_data", [])
    data_b = state.get("source_b_data", [])

    if not data_a or not data_b:
        return {"error": "Missing data from one or both sources"}

    anomalies = []
    matches = 0
    mismatches = 0

    for record_a in data_a:
        record_id = record_a.get("id")
        record_b = next((r for r in data_b if r.get("id") == record_id), None)
        if not record_b:
            mismatches += 1
            continue

        for a_field, b_field in mappings.items():
            a_table, a_col = a_field.split(".") if "." in a_field else ("", a_field)
            b_table, b_col = b_field.split(".") if "." in b_field else ("", b_field)

            a_val = record_a.get(a_col)
            b_val = record_b.get(b_col)

            if a_val is None and b_val is None:
                matches += 1
            elif a_val != b_val:
                mismatches += 1
                anomalies.append({
                    "field_name": a_col,
                    "severity": "high" if a_val is not None and b_val is not None else "medium",
                    "source_a_value": a_val,
                    "source_b_value": b_val,
                    "record_id": record_id,
                })

    total_fields = sum(len(data_a[0].keys()) if data_a else 0, 0)
    return {
        "comparison_results": {
            "total_records": len(data_a),
            "fields_compared": len(mappings),
            "matches": matches,
            "mismatches": mismatches,
            "match_rate": round(matches / max(matches + mismatches, 1), 4),
        },
        "anomalies": anomalies,
        "error": None,
    }


# Build the LangGraph
workflow = StateGraph(ScannerState)
workflow.add_node("fetch_source_data", fetch_source_data)
workflow.add_node("compare_values", compare_values)

workflow.set_entry_point("fetch_source_data")
workflow.add_edge("fetch_source_data", "compare_values")
workflow.add_edge("compare_values", END)

consistency_scanner = workflow.compile()


async def run_consistency_scan(
    source_a_id: str,
    source_b_id: str,
    field_mappings: dict[str, str],
) -> dict[str, Any]:
    """Run the consistency scanning agent."""
    initial_state: ScannerState = {
        "source_a_id": source_a_id,
        "source_b_id": source_b_id,
        "field_mappings": field_mappings,
        "source_a_data": None,
        "source_b_data": None,
        "comparison_results": None,
        "anomalies": [],
        "error": None,
    }
    result = await consistency_scanner.ainvoke(initial_state)
    return result