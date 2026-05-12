# CSRF Attack & Defense Demo

A practical Flask web application designed to demonstrate CSRF vulnerabilities, secure and insecure workflows, and the difference between normal app navigation and attacker-crafted payloads.

## What’s inside

- `app/` — Flask application code, database connectors, routes, templates, and static assets.
- `app/database/` — MySQL schema and seed data for users, teams, and tasks.
- `attacks/` — CSRF attack pages that target the demo app.
- `docker-compose.yml` — Docker setup for web and MySQL services.
- `requirements.txt` / `pyproject.toml` — Python dependencies.

## Quick test path

1. `docker compose up --build`
2. `http://localhost:5000/login`
3. log in as `admin` with password : `Admin123!`
4. In new terminal excecute:
```text 
cd attacks
python3 -m http.server 8080  
```
5. click `Launch TaskAI Optimizer`
6. verify backdoor user in admin users table


## Get it running in under 10 minutes

### 1. Prerequisites

- Docker Desktop installed
- `docker compose` available
- A terminal on Windows or WSL

### 2. Start the app

From the repo root:

```powershell
cd D:\CSRF-Attack-and-Defense
docker compose down -v
docker compose up --build
```

This starts:

- `http://localhost:5000` → Flask app
- MySQL database exposed on local port `3307`

### 3. Verify the database

Open a browser and go to:

```text
http://localhost:5000/test-db
```

If the app connects successfully, you’ll see JSON confirming the database.

### 4. Check seed data (optionnal)

Visite to see if the seed data exists

```text
http://localhost:5000/seed-check
```

## Seeded accounts

Use these accounts directly in the login form:

- admin / `Admin123!` *has the unique privilage to manage users*
- resp_equipe / `RespEq123!`
- resp_projet / `RespPr123!`
- guest1 / `Guest1!`
- guest2 / `Guest2!`

Admin can access the user management page; normal users can use tasks and teams.

## How to test the CSRF attack

### 1. Login as admin

Go to `http://localhost:5000/login` and log in with:

- `admin`
- `Admin123!`

### 2. Visit the attacker page

In a real world scenario this page would be sent by the attacker to the admin (after some OSINT) via Email as a legitimate corporation email to try a new tool/function...

```text
file:///path/to/CSRF-Attack-and-Defense/attacks/TaskAI Optimize.html
```

Run it via independent local python http server from the attacks folder

```text
cd attacks  
python3 -m http.server 8080                                                 
```

Visit it on: 
```text
http://localhost:8080/                                               
```

### 3. Trigger the attack

Click **Launch TaskAI Optimizer**.

What happens:

- the page submits a hidden request to `http://localhost:5000/admin/users/create`
- the request runs silently in the background with the admin session cookies
- the victim sees only a fake IT error message
- the attacker creates an admin backdoor account without visible redirect

*In a real world scenario to find the vulnerable url the attacker could:
1. Inspect the Frontend 
 
```text
<!-- They just right-click → View Page Source -->
<form action="/admin/users/create" method="POST">
```

2. Intercept Traffic (Proxy Tools) : Tools like Burp Suite or OWASP ZAP sit between browser and server.

3. Directory & Endpoint Brute-Forcing : Tools like ffuf, gobuster, dirb:

```bash
# Common wordlists for API endpoints
gobuster dir -u https://target.com -w /usr/share/wordlists/api-endpoints.txt

# Results:
# /admin/users/create (Status: 403)  ← exists but forbidden
# /admin/users/       (Status: 200)
# /api/v1/users       (Status: 200)
```

4. Common Conventions & Framework Defaults

```python
# Django default admin
/admin/

# Rails RESTful routes
/users/new
/users/create
/users/1/edit

# Flask common patterns
/admin/users/create
/api/v1/users
/dashboard/settings
```

5. Framework Leakage & Error Messages

```json
// Debug mode left on? Full route dump:
{
  "error": "Route /admin/users/create not found",
  "available_routes": [
    "/admin/users/create",
    "/admin/users/delete/{id}",
    "/admin/settings"
  ]
}
```

6. Public Information (OSINT): GitHub → Developer pushed code with routes visible

### 4. Confirm the attack

After clicking, open the real app and navigate to:

- `http://localhost:5000/admin/users`

You should see the new injected user if the attack worked.


## Notes for defenders

- The vulnerable endpoint is `POST /admin/users/create`.
- The attack succeeds because it accepts cross-origin POSTs and uses admin session cookies.
- In the real app, the “Launch TaskAI Optimizer” page is a fake phishing page that pretends to be a corporate tool.


---