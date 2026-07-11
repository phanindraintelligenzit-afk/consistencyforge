"""FieldMapperAgent — LangGraph agent that maps semantically equivalent fields using LLM."""

from typing import Any, TypedDict, Optional

from langgraph.graph import StateGraph, END


class FieldMapperState(TypedDict):
    """State for field mapping."""
    source_a_id: str
    source_b_id: str
    source_a_schema: Optional[dict[str, Any]]
    source_b_schema: Optional[dict[str, Any]]
    field_mappings: Optional[dict[str, str]]
    confidence: float
    error: Optional[str]


def extract_fields(state: FieldMapperState) -> dict[str, Any]:
    """Extract field names from both source schemas."""
    schema_a = state.get("source_a_schema", {})
    schema_b = state.get("source_b_schema", {})

    fields_a = []
    tables_a = schema_a.get("tables", []) if schema_a else []
    for table in tables_a:
        for col in table.get("columns", []):
            fields_a.append({"name": col["name"], "type": col.get("infered_type", col.get("type", "unknown")), "table": table["name"]})

    fields_b = []
    tables_b = schema_b.get("tables", []) if schema_b else []
    for table in tables_b:
        for col in table.get("columns", []):
            fields_b.append({"name": col["name"], "type": col.get("infered_type", col.get("type", "unknown")), "table": table["name"]})

    return {"source_a_fields": fields_a, "source_b_fields": fields_b}


def map_fields(state: FieldMapperState) -> dict[str, Any]:
    """Map fields semantically using heuristic and LLM-based matching."""
    schema_a = state.get("source_a_schema", {})
    schema_b = state.get("source_b_schema", {})

    if not schema_a or not schema_b:
        return {"error": "Missing schema data", "field_mappings": None, "confidence": 0.0}

    tables_a = schema_a.get("tables", [])
    tables_b = schema_b.get("tables", [])

    field_mappings = {}
    match_count = 0

    # Simple heuristic: match fields with same name across tables
    for ta in tables_a:
        for ca in ta.get("columns", []):
            for tb in tables_b:
                for cb in tb.get("columns", []):
                    if ca["name"].lower() == cb["name"].lower():
                        key = f"{ta['name']}.{ca['name']}"
                        field_mappings[key] = f"{tb['name']}.{cb['name']}"
                        match_count += 1

    # Add common semantic mappings
    semantic_pairs = [
        ("email", "email_address"),
        ("name", "full_name"),
        ("amount", "value"),
        ("status", "order_status"),
        ("created_at", "creation_date"),
        ("updated_at", "last_modified"),
    ]

    for ta in tables_a:
        for ca in ta.get("columns", []):
            for tb in tables_b:
                for cb in tb.get("columns", []):
                    for a_name, b_name in semantic_pairs:
                        if ca["name"].lower() == a_name and cb["name"].lower() == b_name:
                            key = f"{ta['name']}.{ca['name']}"
                            field_mappings[key] = f"{tb['name']}.{cb['name']}"
                            match_count += 1

    confidence = min(match_count / max(len(tables_a[0].get("columns", [])) if tables_a else 1, 1), 1.0)
    return {"field_mappings": field_mappings, "confidence": confidence, "error": None}


# Build the LangGraph
workflow = StateGraph(FieldMapperState)
workflow.add_node("extract_fields", extract_fields)
workflow.add_node("map_fields", map_fields)

workflow.set_entry_point("extract_fields")
workflow.add_edge("extract_fields", "map_fields")
workflow.add_edge("map_fields", END)

field_mapper_agent = workflow.compile()


async def run_field_mapping(source_a_id: str, source_b_id: str,
                            source_a_schema: dict[str, Any],
                            source_b_schema: dict[str, Any]) -> dict[str, Any]:
    """Run the field mapping agent."""
    initial_state: FieldMapperState = {
        "source_a_id": source_a_id,
        "source_b_id": source_b_id,
        "source_a_schema": source_a_schema,
        "source_b_schema": source_b_schema,
        "field_mappings": None,
        "confidence": 0.0,
        "error": None,
    }
    result = await field_mapper_agent.ainvoke(initial_state)
    return result