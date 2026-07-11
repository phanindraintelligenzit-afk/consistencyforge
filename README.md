# ConsistencyForge

**AI-Powered Cross-System Data Consistency Engine**

[![Build Status](https://github.com/phanindraintelligenzit-afk/consistencyforge/actions/workflows/ci.yml/badge.svg)](https://github.com/phanindraintelligenzit-afk/consistencyforge/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/phanindraintelligenzit-afk/consistencyforge/releases/tag/v1.0.0)
[![Python](https://img.shields.io/badge/python-3.12-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-teal)](https://fastapi.tiangolo.com/)

---

ConsistencyForge is a comprehensive, AI-driven platform for detecting, analyzing, and resolving data inconsistencies across heterogeneous systems. By combining a multi-agent LangGraph pipeline with a modern FastAPI backend and React dashboard, it automates the entire consistency lifecycle — from schema ingestion and field mapping through anomaly scanning, root cause analysis, auto-healing, and reconciliation orchestration.

Modern enterprises operate dozens of data systems (CRM, ERP, data warehouses, SaaS platforms) that often drift out of sync. Manually tracing inconsistencies is slow, error-prone, and doesn't scale. ConsistencyForge replaces ad-hoc debugging with an intelligent, auditable, and automated consistency management workflow.

Built with production-grade infrastructure — PostgreSQL for durable storage, Redis for job queuing and caching, Celery for background task processing, and Docker Compose for one-command deployment — ConsistencyForge is designed to be deployed alongside existing data pipelines with minimal friction.

## Key Features

- **🤖 7 Specialized LangGraph Agents** — A modular AI pipeline covering schema ingestion, field mapping, consistency scanning, root cause analysis, auto-healing, reconciliation orchestration, and audit trail logging.
- **🔗 Multi-Source Support** — Connect REST APIs, PostgreSQL, MySQL, CSV sources, and more. Each source is fully configurable with connection metadata and schema snapshots.
- **⚡ Automated Consistency Checks** — Run on-demand or scheduled cross-system comparisons. Detect value mismatches, missing records, and cardinality violations.
- **🧠 LLM-Powered Field Mapping** — Use LLMs (OpenAI GPT-4o, etc.) to semantically map equivalent fields across disparate systems with confidence scoring.
- **🩺 Root Cause Analysis** — Each anomaly is analyzed to determine its upstream cause — data entry errors, sync delays, transformer bugs, or configuration drift.
- **🔧 Auto-Healing & Reconciliation** — High-confidence anomalies can be auto-resolved; low-confidence cases create human-in-the-loop tickets. Configurable conflict resolution strategies (source-of-truth, latest-wins, majority-vote).
- **📊 Real-Time Dashboard** — React/TypeScript dashboard with anomaly charts, source status, consistency summaries, and timeline visualizations.
- **🔐 JWT Authentication** — Secure API access with role-based user management.
- **📋 Full Audit Trail** — Every check, anomaly, and resolution action is logged for compliance and post-mortem analysis.

## Architecture Overview

ConsistencyForge's core is a pipeline of seven LangGraph agents that process data through a structured workflow:

```
┌──────────────────────────────────────────────────────────────────┐
│                     Frontend (React / TypeScript)                  │
│             Dashboard · Sources · Checks · Anomalies               │
└─────────────────────────────┬────────────────────────────────────┘
                              │ HTTP (REST API)
┌─────────────────────────────▼────────────────────────────────────┐
│                       Backend (FastAPI / Python)                   │
│  ┌──────────┐  ┌──────────┐  ┌──────────────┐  ┌─────────────┐  │
│  │  Auth    │  │ Sources  │  │ Consistency  │  │  Dashboard  │  │
│  │  Routes  │  │  Routes  │  │   Routes     │  │   Routes    │  │
│  └──────────┘  └──────────┘  └──────────────┘  └─────────────┘  │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │               LangGraph AI Agent Pipeline                     │  │
│  │                                                               │  │
│  │  1. SchemaIngestionAgent                                       │  │
│  │     └─ Parses schema definitions from connected data sources  │  │
│  │                                                               │  │
│  │  2. FieldMapperAgent                                           │  │
│  │     └─ Maps semantically equivalent fields using LLM matching │  │
│  │                                                               │  │
│  │  3. ConsistencyScannerAgent                                    │  │
│  │     └─ Executes cross-system queries and detects mismatches   │  │
│  │                                                               │  │
│  │  4. RootCauseAgent                                             │  │
│  │     └─ Analyzes anomaly root causes with confidence scoring   │  │
│  │                                                               │  │
│  │  5. AutoHealAgent                                              │  │
│  │     └─ Proposes and executes automated anomaly fixes          │  │
│  │                                                               │  │
│  │  6. ReconciliationOrchestratorAgent                            │  │
│  │     └─ Coordinates multi-step reconciliation workflows        │  │
│  │                                                               │  │
│  │  7. AuditTrailAgent                                            │  │
│  │     └─ Logs actions and builds compliance-ready audit trails  │  │
│  └─────────────────────────────────────────────────────────────┘  │
└─────────────────────────────┬────────────────────────────────────┘
                              │
     ┌────────────────────────┼────────────────────────┐
     ▼                        ▼                        ▼
┌────────────┐         ┌────────────┐          ┌──────────────┐
│ PostgreSQL │         │   Redis    │          │    Other     │
│  (Data)    │         │ (Queue)    │          │   Sources    │
└────────────┘         └────────────┘          └──────────────┘
```

### The 7 LangGraph Agents in Detail

| # | Agent | Role | Key Capabilities |
|---|-------|------|------------------|
| 1 | **SchemaIngestionAgent** | Schema Discovery | Ingests schema definitions from REST APIs, DB dumps, and config; normalizes into unified representation; detects field types, relationships, and constraints |
| 2 | **FieldMapperAgent** | Semantic Mapping | Maps semantically equivalent fields (e.g. `cust_id` ↔ `customerNumber`); uses LLM for semantic equivalence with confidence scoring |
| 3 | **ConsistencyScannerAgent** | Cross-System Comparison | Executes cross-system queries on mapped fields; detects value differences, missing records, and cardinality violations; generates structured anomaly reports |
| 4 | **RootCauseAgent** | Diagnosis | Analyzes each anomaly to determine root cause (data entry error, sync delay, transformer bug); traverses dependency graph to find upstream origin |
| 5 | **AutoHealAgent** | Remediation | Proposes and optionally auto-executes fixes; high-confidence → writes correction; low-confidence → creates human-in-the-loop ticket |
| 6 | **ReconciliationOrchestratorAgent** | Workflow Orchestration | Coordinates multi-step reconciliation; selects conflict resolution strategy; manages retry policies and dead-letter handling |
| 7 | **AuditTrailAgent** | Compliance | Logs every check, anomaly, and action; builds compliance-ready audit trails; produces periodic consistency summary reports |

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend Framework** | Python 3.12, FastAPI, Uvicorn |
| **ORM** | SQLAlchemy 2.0 (async) with asyncpg |
| **AI Agents** | LangGraph, LangChain, OpenAI |
| **Task Queue** | Celery with Redis broker |
| **Database** | PostgreSQL 16 |
| **Cache / Queue** | Redis 7 |
| **Frontend** | React 18, TypeScript, Vite |
| **UI / Charts** | Tailwind CSS, Recharts |
| **State / Data Fetching** | React Query, Axios |
| **API Documentation** | OpenAPI / Swagger (auto-generated) |
| **Auth** | JWT (python-jose, passlib/bcrypt) |
| **Infrastructure** | Docker, Docker Compose, Nginx |

## Quick Start

### Prerequisites

- Docker and Docker Compose (v2+)
- Git

### One-Command Launch

```bash
git clone https://github.com/phanindraintelligenzit-afk/consistencyforge.git
cd consistencyforge
docker-compose up -d
```

This starts five services:
- **PostgreSQL 16** — Primary data store
- **Redis 7** — Celery broker and cache
- **Backend API** — FastAPI on port 8000
- **Celery Worker** — Background task processing
- **Frontend** — Nginx-served React app on port 80

### Access the Application

| Service | URL |
|---------|-----|
| Frontend Dashboard | [http://localhost](http://localhost) |
| Backend API | [http://localhost:8000](http://localhost:8000) |
| API Swagger Docs | [http://localhost:8000/docs](http://localhost:8000/docs) |
| API ReDoc | [http://localhost:8000/redoc](http://localhost:8000/redoc) |

### Local Development (without Docker)

```bash
# Backend
cd backend
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend (separate terminal)
cd frontend
npm install
npm run dev
```

## API Documentation

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Register a new user |
| POST | `/api/auth/login` | Login and receive JWT |
| GET | `/api/auth/me` | Get current user profile |

### Data Sources

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/sources/` | List all connected data sources |
| POST | `/api/sources/` | Register a new data source |
| GET | `/api/sources/{id}` | Get source details including schema |
| DELETE | `/api/sources/{id}` | Remove a data source |
| POST | `/api/sources/{id}/sync` | Trigger schema re-sync for a source |

### Consistency Checks

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/consistency/checks` | List all consistency checks |
| POST | `/api/consistency/checks` | Run a new consistency check |
| GET | `/api/consistency/anomalies` | List all detected anomalies |
| PUT | `/api/consistency/anomalies/{id}/resolve` | Resolve or heal an anomaly |

### Agents

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/agents/` | List available AI agents and their status |

### Dashboard

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/dashboard/summary` | Aggregate dashboard statistics |

### System

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Health check (returns status, service name, version) |

Full interactive documentation is available at [http://localhost:8000/docs](http://localhost:8000/docs) when the backend is running.

## Project Structure

```
consistencyforge/
├── backend/
│   ├── app/
│   │   ├── api/                  # FastAPI route handlers
│   │   │   ├── auth.py          # Authentication endpoints
│   │   │   ├── sources.py       # Data source CRUD
│   │   │   ├── consistency.py   # Consistency check routes
│   │   │   ├── dashboard.py     # Dashboard stats
│   │   │   └── agents.py        # Agent status endpoints
│   │   ├── agents/               # LangGraph AI agents
│   │   │   ├── schema_ingestion.py
│   │   │   ├── field_mapper.py
│   │   │   ├── consistency_scanner.py
│   │   │   ├── root_cause.py
│   │   │   ├── auto_heal.py
│   │   │   ├── reconciliation_orchestrator.py
│   │   │   └── audit_trail.py
│   │   ├── core/                 # Configuration & infrastructure
│   │   │   ├── config.py        # Pydantic settings
│   │   │   ├── database.py      # SQLAlchemy engine & session
│   │   │   └── security.py      # JWT & password utilities
│   │   ├── models/               # SQLAlchemy ORM models
│   │   │   ├── datasource.py
│   │   │   ├── field_mapping.py
│   │   │   ├── consistency_check.py
│   │   │   ├── anomaly.py
│   │   │   ├── agent_log.py
│   │   │   └── audit_log.py
│   │   ├── schemas/              # Pydantic request/response models
│   │   │   ├── auth.py
│   │   │   ├── source.py
│   │   │   ├── consistency.py
│   │   │   └── dashboard.py
│   │   ├── services/             # Business logic layer
│   │   │   ├── source_service.py
│   │   │   └── consistency_service.py
│   │   ├── celery_app.py         # Celery worker configuration
│   │   └── main.py               # FastAPI application entry point
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── api/                  # API client modules
│   │   │   ├── client.ts        # Axios instance with auth
│   │   │   ├── auth.ts
│   │   │   ├── sources.ts
│   │   │   ├── consistency.ts
│   │   │   └── dashboard.ts
│   │   ├── components/           # Reusable React components
│   │   │   ├── Layout.tsx
│   │   │   ├── StatsCard.tsx
│   │   │   ├── SourceCard.tsx
│   │   │   ├── AddSourceModal.tsx
│   │   │   ├── AnomalyChart.tsx
│   │   │   └── AnomalyRow.tsx
│   │   ├── pages/                # Route-level page components
│   │   │   ├── DashboardPage.tsx
│   │   │   ├── SourcesPage.tsx
│   │   │   ├── ChecksPage.tsx
│   │   │   ├── AnomaliesPage.tsx
│   │   │   └── LoginPage.tsx
│   │   ├── context/              # React context providers
│   │   │   └── AuthContext.tsx
│   │   ├── App.tsx               # Root app with routing
│   │   ├── main.tsx              # Entry point
│   │   └── index.css             # Tailwind CSS imports
│   ├── Dockerfile
│   ├── nginx.conf
│   ├── package.json
│   ├── vite.config.ts
│   ├── tsconfig.json
│   └── tailwind.config.js
├── docker-compose.yml
├── ARCHITECTURE.md
├── CONTRIBUTING.md
├── SECURITY.md
├── LICENSE
└── README.md
```

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines on:

- Setting up a development environment
- Coding standards and linting
- Testing requirements
- Pull request process
- Code review checklist

## Security

View our security policy in [SECURITY.md](SECURITY.md) for instructions on reporting vulnerabilities and our supported version scope.

## License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.