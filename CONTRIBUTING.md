# Contributing to ConsistencyForge

We're thrilled you're interested in contributing to ConsistencyForge! Whether you're fixing a bug, adding a feature, improving documentation, or anything in between — your help is welcome.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Environment](#development-environment)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Pull Request Process](#pull-request-process)
- [Code Review Checklist](#code-review-checklist)
- [Feature Requests and Bug Reports](#feature-requests-and-bug-reports)

## Code of Conduct

This project adheres to the [Contributor Covenant](https://www.contributor-covenant.org/). By participating, you agree to maintain a respectful, inclusive, and harassment-free environment. Please report unacceptable behavior to the project maintainers.

## Getting Started

1. **Fork the repository** on GitHub.
2. **Clone your fork:**
   ```bash
   git clone https://github.com/your-username/consistencyforge.git
   cd consistencyforge
   ```
3. **Add the upstream remote:**
   ```bash
   git remote add upstream https://github.com/phanindraintelligenzit-afk/consistencyforge.git
   ```
4. **Create a feature branch:**
   ```bash
   git checkout -b feat/your-feature-name
   ```

## Development Environment

### Backend Setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Frontend Setup

```bash
cd frontend
npm install
```

### Full-Stack with Docker (recommended for integration testing)

```bash
docker-compose up -d
```

### Environment Variables

Copy the backend `.env` template:

```bash
cp backend/.env.example backend/.env  # if available
```

Key variables:
| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | `postgresql+asyncpg://...` | PostgreSQL connection string |
| `JWT_SECRET` | — | Secret key for JWT tokens |
| `OPENAI_API_KEY` | — | OpenAI API key for LLM agents |
| `REDIS_URL` | `redis://localhost:6379/0` | Redis connection |

## Coding Standards

### Python (Backend)

- **Python version**: 3.12+
- **Formatter**: [Black](https://github.com/psf/black) with default settings
- **Linter**: [Flake8](https://flake8.pycqa.org/) with max line length 120
- **Type hints**: Required for all function signatures
- **Docstrings**: Google or NumPy style for public modules, classes, and functions
- **Imports**: Grouped as standard library → third-party → local (separated by blank line)

```python
import json
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.models.datasource import DataSource
```

### TypeScript / React (Frontend)

- **Formatting**: [Prettier](https://prettier.io/) with default config
- **Linting**: ESLint with TypeScript rules
- **Components**: Functional components with hooks (no class components)
- **Naming**: `PascalCase` for components, `camelCase` for variables/functions, `UPPER_CASE` for constants
- **State management**: React Query for server state, React Context for auth/global state
- **Styling**: Tailwind CSS utility classes; avoid inline styles

### Git Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <description>

[optional body]
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`, `perf`, `ci`, `build`.

Examples:
```
feat(agents): add field mapper confidence threshold parameter
fix(api): handle null source config in sync endpoint
docs(readme): update quick start with new env vars
test(backend): add unit tests for root cause agent
```

## Testing

### Backend

We use `pytest` with `pytest-asyncio` for async tests.

```bash
cd backend
pip install pytest pytest-asyncio httpx

# Run all tests
pytest -v --asyncio-mode=auto

# Run with coverage
pytest --cov=app --cov-report=term-missing
```

Tests live alongside the module they test (e.g., `tests/test_agents/`) or in a top-level `tests/` directory. Each test file should be prefixed with `test_`.

### Frontend

```bash
cd frontend
npm test          # or the configured test runner
```

### Running the Full CI Pipeline Locally

```bash
# Python lint
cd backend && flake8 app/ --max-line-length=120

# Backend verification
python -c "from app.main import app; print('OK')"

# Frontend build
cd frontend && npm run build
```

## Pull Request Process

1. **Ensure your branch is up to date:**
   ```bash
   git fetch upstream
   git rebase upstream/master
   ```

2. **Run all checks locally** — lint, test, and build must pass.

3. **Push your branch** and open a pull request against `master`:
   ```bash
   git push origin feat/your-feature-name
   ```

4. **Fill out the PR template** (if one exists). Include:
   - What the change does
   - Why it's needed
   - How it was tested
   - Screenshots for UI changes

5. **Request review** from at least one maintainer.

6. **Address feedback** — keep the commit history clean. Use `git commit --amend` and `git push --force` on your feature branch as needed.

7. **Squash commits** before merge — your final commit message should follow conventional commits format.

## Code Review Checklist

Reviewers will check for:

- [ ] Code follows the project's style and conventions
- [ ] Type hints present and correct
- [ ] Tests cover the new functionality or bug fix
- [ ] All existing tests pass
- [ ] API changes are documented (OpenAPI schemas, README)
- [ ] No hardcoded secrets or credentials
- [ ] Database migrations (if applicable) are backward-compatible
- [ ] Error handling is appropriate — no bare `except:` clauses
- [ ] Logging is added for key operations
- [ ] UI changes are responsive and follow Tailwind conventions

## Feature Requests and Bug Reports

- **Bug reports**: Open a GitHub issue with the `bug` label. Include steps to reproduce, expected vs. actual behavior, environment details, and logs if applicable.
- **Feature requests**: Open a GitHub issue with the `enhancement` label. Describe the problem you're solving, proposed solution, and any alternatives considered.
- **Security vulnerabilities**: Do NOT open a public issue. Follow the disclosure process in [SECURITY.md](SECURITY.md).

---

Thank you for contributing to ConsistencyForge! 🚀