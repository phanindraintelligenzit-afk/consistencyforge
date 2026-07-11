# Security Policy for ConsistencyForge

## Supported Versions

The following versions of ConsistencyForge are currently supported with security updates:

| Version | Supported          |
|---------|--------------------|
| 1.0.x   | ✅ Active support |
| < 1.0   | ❌ Not supported  |

## Reporting a Vulnerability

We take the security of ConsistencyForge seriously. If you discover a security vulnerability, please follow the responsible disclosure process below.

**Do NOT report security vulnerabilities through public GitHub issues, discussions, or pull requests.** Please send reports via email to the project maintainers.

### How to Report

1. **Email** the details to the project's security contact (available from the repository's security insights tab or by reaching out to a maintainer).
2. **Include** as much of the following as possible:
   - Type of vulnerability (e.g., SQL injection, XSS, authentication bypass)
   - Steps to reproduce the issue
   - Affected versions and components
   - Proof of concept or exploit code (if available)
   - Potential impact
   - Suggested fix (if known)

### What to Expect

- **Acknowledgment**: You will receive an acknowledgment of your report within 48 hours.
- **Investigation**: The maintainers will investigate and validate the vulnerability. We'll keep you informed of progress.
- **Fix timeline**: A fix will be developed and released as soon as possible, depending on severity:
  - **Critical**: Patch release within 72 hours
  - **High**: Patch release within 7 days
  - **Medium**: Patch release within 30 days
  - **Low**: Scheduled for next minor release
- **Disclosure**: We will coordinate public disclosure with you. We typically publish a security advisory on GitHub once the fix is released.

## Scope

The following components are in scope for security reports:

- Backend API (`backend/`) — FastAPI application, authentication, database access
- Frontend application (`frontend/`) — React SPA, API client, XSS/CSRF concerns
- Docker configurations — Container security, exposed ports, secrets management
- CI/CD pipeline — GitHub Actions workflows, artifact security
- Dependencies — Third-party packages and their known vulnerabilities

The following are **out of scope**:

- Issues in dependencies that have already been patched upstream
- Theoretical attacks without a practical proof of concept
- Social engineering attacks against project contributors
- Denial of service attacks on infrastructure we don't control

## Security Best Practices for Deployment

When deploying ConsistencyForge to production, follow these security guidelines:

### 🔑 Secrets Management

- **Never** hardcode secrets in source code or Dockerfiles
- Use environment variables or a secrets manager (e.g., HashiCorp Vault, AWS Secrets Manager)
- Generate a strong random `JWT_SECRET`:
  ```bash
  openssl rand -hex 32
  ```
- Rotate secrets regularly

### 🗄️ Database

- Use strong, unique passwords for PostgreSQL
- Enable SSL/TLS for database connections
- Restrict database access to only the backend service (not exposed publicly)
- Run regular backups and test restoration

### 🌐 Network

- Place all services behind a reverse proxy with TLS (Nginx, Caddy, Traefik)
- Use HTTPS in production — never expose the API over plain HTTP
- Configure CORS to allow only your frontend origin
- Use a Web Application Firewall (WAF) for additional protection

### 🔒 Authentication

- Enforce strong password policies
- Use short-lived JWT tokens (default: 60 minutes) with refresh token rotation
- Implement rate limiting on auth endpoints
- Use role-based access control (RBAC) for multi-tenant deployments

### 📦 Dependencies

- Regularly update dependencies:
  ```bash
  # Backend
  cd backend && pip list --outdated
  
  # Frontend
  cd frontend && npm audit
  ```
- Use lockfiles (`package-lock.json`, `requirements.txt` pinned versions)
- Monitor for CVEs using GitHub Dependabot or similar tools

### 📝 Logging

- Log security-relevant events: authentication attempts, authorization failures, data mutations
- Never log sensitive data (passwords, tokens, PII)
- Use structured logging for easier audit analysis

## Dependency Vulnerability Reporting

If you find a vulnerable dependency:

1. Check if there's already a fix available upstream
2. If a patched version exists, update the dependency and submit a PR
3. If no patch exists, follow the reporting process above

We use GitHub Dependabot for automated dependency monitoring. You can enable it in your fork via **Settings → Security → Dependabot alerts**.

## Acknowledgments

We appreciate the security community's help in keeping ConsistencyForge safe. Contributors who report valid vulnerabilities will be acknowledged in release notes (unless they prefer anonymity).

---

*This security policy is maintained by the ConsistencyForge maintainers and will be updated as the project evolves.*