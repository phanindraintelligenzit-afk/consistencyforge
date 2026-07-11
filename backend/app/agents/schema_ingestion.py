"""SchemaIngestionAgent — LangGraph agent that parses schema definitions from data source configs."""

from typing import Any, TypedDict, Optional

from langgraph.graph import StateGraph, END


class SchemaIngestionState(TypedDict):
    """State for schema ingestion."""
    source_id: str
    source_type: str
    connection_config: dict[str, Any]
    raw_schema: Optional[dict[str, Any]]
    parsed_schema: Optional[dict[str, Any]]
    error: Optional[str]


def parse_connection(state: SchemaIngestionState) -> dict[str, Any]:
    """Extract connection details from config."""
    config = state["connection_config"]
    return {
        "host": config.get("host", "localhost"),
        "port": config.get("port", 5432),
        "database": config.get("database", ""),
        "username": config.get("username", ""),
    }


def discover_schema(state: SchemaIngestionState) -> dict[str, Any]:
    """Simulate schema discovery from the data source."""
    source_type = state["source_type"]
    # In production, this would connect to the actual source
    if source_type == "postgresql":
        raw_schema = {
            "tables": [
                {
                    "name": "users",
                    "columns": [
                        {"name": "id", "type": "integer", "nullable": False},
                        {"name": "email", "type": "varchar(255)", "nullable": False},
                        {"name": "name", "type": "varchar(255)", "nullable": True},
                        {"name": "created_at", "type": "timestamp", "nullable": False},
                    ],
                },
                {
                    "name": "orders",
                    "columns": [
                        {"name": "id", "type": "integer", "nullable": False},
                        {"name": "user_id", "type": "integer", "nullable": False},
                        {"name": "amount", "type": "decimal", "nullable": False},
                        {"name": "status", "type": "varchar(50)", "nullable": True},
                    ],
                },
            ]
        }
    elif source_type == "csv":
        raw_schema = {
            "tables": [
                {
                    "name": "data",
                    "columns": [
                        {"name": "id", "type": "string", "nullable": False},
                        {"name": "value", "type": "number", "nullable": True},
                        {"name": "label", "type": "string", "nullable": True},
                    ],
                }
            ]
        }
    else:
        raw_schema = {
            "tables": [
                {
                    "name": "records",
                    "columns": [
                        {"name": "id", "type": "string", "nullable": False},
                        {"name": "data", "type": "jsonb", "nullable": True},
                    ],
                }
            ]
        }
    return {"raw_schema": raw_schema}


def parse_schema(state: SchemaIngestionState) -> dict[str, Any]:
    """Parse raw schema into normalized format."""
    raw = state["raw_schema"]
    if not raw:
        return {"error": "No raw schema available", "parsed_schema": None}

    parsed = {
        "source_type": state["source_type"],
        "table_count": len(raw.get("tables", [])),
        "tables": [],
    }
    for table in raw.get("tables", []):
        parsed["tables"].append({
            "name": table["name"],
            "columns": [
                {
                    "name": col["name"],
                    "type": col["type"],
                    "nullable": col.get("nullable", True),
                    "infered_type": "numeric" if "decimal" in col["type"].lower() or col["type"] == "number" else "text" if "varchar" in col["type"].lower() or col["type"] == "string" else "datetime" if "timestamp" in col["type"].lower() else "other",
                }
                for col in table.get("columns", [])
            ],
        })
    return {"parsed_schema": parsed, "error": None}


# Build the LangGraph
workflow = StateGraph(SchemaIngestionState)
workflow.add_node("parse_connection", parse_connection)
workflow.add_node("discover_schema", discover_schema)
workflow.add_node("parse_schema", parse_schema)

workflow.set_entry_point("parse_connection")
workflow.add_edge("parse_connection", "discover_schema")
workflow.add_edge("discover_schema", "parse_schema")
workflow.add_edge("parse_schema", END)

schema_ingestion_agent = workflow.compile()


async def run_schema_ingestion(source_id: str, source_type: str, connection_config: dict[str, Any]) -> dict[str, Any]:
    """Run the schema ingestion agent."""
    initial_state: SchemaIngestionState = {
        "source_id": source_id,
        "source_type": source_type,
        "connection_config": connection_config,
        "raw_schema": None,
        "parsed_schema": None,
        "error": None,
    }
    result = await schema_ingestion_agent.ainvoke(initial_state)
    return result