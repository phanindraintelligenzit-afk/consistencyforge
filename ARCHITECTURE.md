# ConsistencyForge — Architecture Blueprint

## Tech Stack
- **Backend:** Python 3.12, FastAPI, SQLAlchemy 2.0, PostgreSQL
- **Agents:** LangGraph (7 specialized agents), LangChain
- **Frontend:** React 18, TypeScript, Tailwind CSS, React Query, Recharts
- **Infrastructure:** Docker, Docker Compose, Nginx, Redis (caching/queue)
- **Auth:** JWT-based with role-based access control

## API Design

### Core Endpoints
```
POST   /api/v1/auth/login
POST   /api/v1/auth/register
GET    /api/v1/sources                    # List connected data sources
POST   /api/v1/sources                    # Register a new source
DELETE /api/v1/sources/{id}               # Remove source
POST   /api/v1/sources/{id}/sync          # Trigger sync

GET    /api/v1/consistency/checks         # List consistency checks
POST   /api/v1/consistency/checks         # Run a consistency check
GET    /api/v1/consistency/checks/{id}    # Get check result
GET    /api/v1/consistency/anomalies      # List all anomalies
PATCH  /api/v1/consistency/anomalies/{id} # Resolve/heal anomaly

GET    /api/v1/agents/status             # Agent health dashboard
POST   /api/v1/agents/reconcile          # Manual reconcile trigger

GET    /api/v1/dashboard/summary         # Dashboard stats
GET    /api/v1/dashboard/timeline        # Anomaly timeline

GET    /api/v1/logs                      # Audit log
```

## 7 LangGraph Agents

### 1. SchemaIngestionAgent
- Ingests schema definitions from connected data sources (REST APIs, DB dumps, CSV definitions)
- Normalizes schemas into a unified representation
- Detects field types, relationships, and constraints

### 2. FieldMapperAgent
- Maps semantically equivalent fields across systems (e.g. "cust_id" ↔ "customerNumber")
- Uses LLM to understand semantic equivalence
- Returns confidence scores for each mapping

### 3. ConsistencyScannerAgent  
- Executes cross-system queries comparing mapped fields
- Detects mismatches: value differences, missing records, cardinality violations
- Generates structured anomaly reports

### 4. RootCauseAgent
- Analyzes each anomaly to determine root cause (data entry error, sync delay, transformer bug)
- Traverses dependency graph to find upstream origin
- Returns diagnosis with confidence score

### 5. AutoHealAgent
- Proposes and optionally auto-executes fixes for detected anomalies
- For high-confidence matches: writes correction to source system
- For low-confidence: creates human-in-the-loop ticket

### 6. ReconciliationOrchestratorAgent
- Coordinates multi-step reconciliation workflows
- Decides conflict resolution strategy (source-of-truth, latest-wins, majority-vote)
- Manages retry policies and dead-letter handling

### 7. AuditTrailAgent
- Logs every check, anomaly, and action
- Builds compliance-ready audit trails
- Produces periodic consistency summary reports

## Database Schema

```sql
-- Sources connected to the system
CREATE TABLE data_sources (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    source_type VARCHAR(50) NOT NULL,  -- rest_api, postgres, mysql, csv
    connection_config JSONB NOT NULL,
    schema_snapshot JSONB,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);

-- Field mappings between sources
CREATE TABLE field_mappings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_a_id UUID REFERENCES data_sources(id),
    source_b_id UUID REFERENCES data_sources(id),
    source_a_field VARCHAR(255) NOT NULL,
    source_b_field VARCHAR(255) NOT NULL,
    confidence FLOAT DEFAULT 0.0,
    created_at TIMESTAMP DEFAULT now()
);

-- Consistency check runs
CREATE TABLE consistency_checks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255),
    status VARCHAR(50) DEFAULT 'running',  -- running, completed, failed
    total_fields_checked INT DEFAULT 0,
    mismatches_found INT DEFAULT 0,
    auto_healed INT DEFAULT 0,
    started_at TIMESTAMP DEFAULT now(),
    completed_at TIMESTAMP
);

-- Detected anomalies
CREATE TABLE anomalies (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    check_id UUID REFERENCES consistency_checks(id),
    field_mapping_id UUID REFERENCES field_mappings(id),
    source_a_value TEXT,
    source_b_value TEXT,
    severity VARCHAR(20) DEFAULT 'medium',  -- low, medium, high, critical
    anomaly_type VARCHAR(50),  -- value_mismatch, missing_record, cardinality_violation
    status VARCHAR(30) DEFAULT 'open',  -- open, investigating, resolved, ignored
    root_cause TEXT,
    resolution TEXT,
    created_at TIMESTAMP DEFAULT now(),
    resolved_at TIMESTAMP
);

-- Agent run logs
CREATE TABLE agent_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_name VARCHAR(100) NOT NULL,
    check_id UUID REFERENCES consistency_checks(id),
    input_tokens INT,
    output_tokens INT,
    duration_ms INT,
    result JSONB,
    created_at TIMESTAMP DEFAULT now()
);

-- Audit trail
CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    action VARCHAR(100) NOT NULL,
    entity_type VARCHAR(50),
    entity_id UUID,
    actor VARCHAR(255),
    details JSONB,
    created_at TIMESTAMP DEFAULT now()
);
```

## Directory Structure
```
consistencyforge/
├── backend/
│   ├── app/
│   │   ├── api/              # FastAPI route handlers
│   │   ├── agents/           # LangGraph agent definitions
│   │   ├── core/             # Config, auth, database
│   │   ├── models/           # SQLAlchemy models
│   │   ├── schemas/          # Pydantic schemas
│   │   └── services/         # Business logic
│   ├── alembic/              # DB migrations
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── pages/           # Route pages
│   │   ├── api/             # API client
│   │   └── hooks/           # Custom hooks
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```