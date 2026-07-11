# ConsistencyForge

**AI-Powered Cross-System Data Consistency Engine**

ConsistencyForge is a comprehensive solution for detecting, analyzing, and resolving data inconsistencies across heterogeneous systems. It uses a multi-agent AI pipeline built with LangGraph to automate schema ingestion, field mapping, consistency scanning, root cause analysis, auto-healing, and reconciliation orchestration.

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                   Frontend (React/TS)                │
│                 Dashboard · Sources · Checks          │
└──────────────────────┬──────────────────────────────┘
                       │ HTTP (REST API)
┌──────────────────────▼──────────────────────────────┐
│                 Backend (FastAPI/Python)              │
│    ┌──────────┐ ┌──────────┐ ┌──────────────────┐   │
│    │  Auth    │ │ Sources  │ │  Consistency      │   │
│    │  API     │ │  CRUD    │ │  Checks API       │   │
│    └──────────┘ └──────────┘ └──────────────────┘   │
│    ┌──────────────────────────────────────────┐      │
│    │         AI Agent Pipeline (LangGraph)     │      │
│    │  Schema → Field Map → Scan → Root Cause  │      │
│    │  → Auto-Heal → Reconcile → Audit Trail   │      │
│    └──────────────────────────────────────────┘      │
└──────────────────────┬──────────────────────────────┘
                       │
    ┌──────────────────┼──────────────────┐
    ▼                  ▼                  ▼
┌──────────┐    ┌──────────┐     ┌──────────┐
│PostgreSQL│    │  Redis   │     │  Other   │
│ (Data)   │    │ (Queue)  │     │ Sources  │
└──────────┘    └──────────┘     └──────────┘
```

## Tech Stack

- **Backend**: Python 3.12, FastAPI, SQLAlchemy (async), LangGraph, Celery
- **Frontend**: React 18, TypeScript, Vite, Tailwind CSS, Recharts, React Query
- **Infrastructure**: Docker Compose (PostgreSQL, Redis, Nginx)

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Node.js 20+ (for local frontend dev)
- Python 3.12+ (for local backend dev)

### Quick Start (Docker)

```bash
# Clone and start all services
git clone https://github.com/phanindraintelligenzit-afk/consistencyforge.git
cd consistencyforge
docker-compose up -d

# Access the app
# Frontend: http://localhost
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Local Development

```bash
# Backend
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Register new user |
| POST | `/api/auth/login` | Login & get JWT |
| GET | `/api/auth/me` | Current user info |
| GET | `/api/sources/` | List data sources |
| POST | `/api/sources/` | Create data source |
| GET | `/api/sources/{id}` | Get source details |
| DELETE | `/api/sources/{id}` | Delete source |
| POST | `/api/sources/{id}/sync` | Sync source schema |
| POST | `/api/consistency/checks` | Run consistency check |
| GET | `/api/consistency/checks` | List checks |
| GET | `/api/consistency/anomalies` | List anomalies |
| PUT | `/api/consistency/anomalies/{id}/resolve` | Resolve anomaly |
| GET | `/api/dashboard/summary` | Dashboard stats |
| GET | `/api/agents/` | List AI agents |

## AI Agents

ConsistencyForge uses a pipeline of LangGraph-based agents:

1. **SchemaIngestionAgent** — Parses schema definitions from data source configs
2. **FieldMapperAgent** — Maps semantically equivalent fields using heuristic/LLM matching
3. **ConsistencyScannerAgent** — Cross-system value comparison
4. **RootCauseAgent** — Analyzes root causes of anomalies
5. **AutoHealAgent** — Proposes automated fixes
6. **ReconciliationOrchestratorAgent** — Orchestrates the reconciliation workflow
7. **AuditTrailAgent** — Compliance and audit logging

## License

MIT