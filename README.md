# CSRF Attack & Defense Demo

A practical Flask web application designed to demonstrate CSRF vulnerabilities, secure and insecure workflows, and the difference between normal app navigation and attacker-crafted payloads.

## What’s inside

- `app/` — Flask application code, database connectors, routes, templates, and static assets.
- `app/database/` — MySQL schema and seed data for users, teams, and tasks.
- `attacks/` — CSRF attack pages that simulate real-world malicious payload delivery.
- `docker-compose.yml` — Docker setup for web and MySQL services.
- `requirements.txt` / `pyproject.toml` — Python dependencies.

---

## Quick test path

1. Start the stack:
```bash
docker compose up --build
```

2. Open the app:
```text
http://localhost:5000/login
```

3. Login as admin:
- username: `admin`
- password: `Admin123!`

4. In a new terminal:
```bash
cd attacks
python -m http.server 8080
```

5. Open attacker page:
```text
http://localhost:8080/
```

6. Click **Launch TaskAI Optimizer**

7. Verify result:
```text
Admin panel → Users table → check injected user
```

---

## Get it running in under 10 minutes

### 1. Prerequisites

- Docker Desktop installed
- `docker compose` available
- A terminal (Windows / WSL / Linux)

---

### 2. Start the app

From repo root:

```bash
docker compose down -v
docker compose up --build
```

This starts:
- Flask app → http://localhost:5000
- MySQL → internal Docker network

---

### 3. Verify database

```text
http://localhost:5000/test-db
```

Expected: JSON success response

---

### 4. Check seed data (optional)

```text
http://localhost:5000/seed-check
```

---

## Seeded accounts

Use directly in login form:

- admin / `Admin123!` → full privileges (user management)
- resp_equipe / `RespEq123!`
- resp_projet / `RespPr123!`
- guest1 / `Guest1!`
- guest2 / `Guest2!`

---

## CSRF attack flow

### 1. Login as admin
```text
http://localhost:5000/login
```

### 2. Open attacker page

In real-world scenario:
- attacker sends link via email / phishing / OSINT

Local demo:

```bash
cd attacks
python -m http.server 8080
```

Open:
```text
http://localhost:8080/
```

---

### 3. Trigger attack

Click **Launch TaskAI Optimizer**

What happens:

- hidden POST request sent to:
```text
POST /admin/users/create
```

- browser automatically includes admin session cookies
- request is executed without user consent
- attacker creates a new admin-level account

Victim sees:
- fake UI message / harmless page behavior

---

## How attackers find endpoints (theory)

### 1. Frontend inspection
```html
<form action="/admin/users/create" method="POST">
```

### 2. Proxy tools
- Burp Suite
- OWASP ZAP

### 3. Brute-force discovery
```bash
gobuster dir -u https://target.com -w wordlist.txt
```

### 4. Framework conventions
- `/admin/`
- `/api/v1/`
- `/users/create`

### 5. Debug leaks
```json
{
  "available_routes": [
    "/admin/users/create",
    "/admin/users/delete/{id}"
  ]
}
```

### 6. OSINT
- GitHub leaks
- exposed repos
- dev docs

---

## Defense notes

- Vulnerable endpoint:
```text
POST /admin/users/create
```

- Issue:
  - no CSRF token
  - trusts session cookies blindly

- Fix (conceptually):
  - CSRF tokens (Flask-WTF / custom)
  - SameSite cookies
  - origin validation

---

## Goal of this project

This is a **controlled vulnerability lab**, not a production system.

It demonstrates:
- how CSRF works
- how attackers exploit authenticated sessions
- how simple backend assumptions lead to privilege abuse
