# CSRF Attack & Defense Demo

**Branch:** `secure`

This repository is the secure defense branch of the CSRF Attack & Defense project. It contains the Flask application with CSRF protections and related hardening applied. 

## Overview

This demo app is built to show both the attack surface of CSRF and how to defend against it in a real Flask application.

The secure branch includes:
- Global CSRF protection with `Flask-WTF` and `CSRFProtect`
- `SameSite=Lax` session cookies and `HttpOnly` session cookies
- Explicit CSRF tokens injected into all POST forms
- Admin-only restricted user management pages
- Role whitelisting for user creation
- A collection of attacker pages in `attacks/` used to demonstrate how malicious CSRF payloads work against a vulnerable app

## Project structure

- `app/` – Flask application code
  - `app.py` – application factory and configuration
  - `config.py` – environment-backed configuration values
  - `database/` – database connection helper and seed/schema files
  - `routes/` – application blueprints for auth, tasks, teams, and admin
  - `templates/` – HTML templates with CSRF token injection
- `attacks/` – attacker-controlled pages and CSRF payload demos
- `tests/` – automated tests for authentication, CSRF protection, security headers, and task flows
- `requirements.txt` – Python dependencies

## What is defended in this branch

### CSRF protection
- `Flask-WTF` and `CSRFProtect(app)` are enabled globally in `app/app.py`
- All POST forms include `{{ csrf_token() }}` in the template files
- Invalid CSRF submissions result in a 403 error page

### Cookie security
- `SESSION_COOKIE_HTTPONLY = True`
- `SESSION_COOKIE_SAMESITE = 'Lax'`
- `SESSION_COOKIE_SECURE = False` is kept for local HTTP development; enable `True` in HTTPS deployments

### User and admin safeguards
- Only authenticated users can access task and team routes
- Admin routes require `role == 'admin'`
- User creation uses strict role whitelisting and rejects unexpected values
- Users cannot delete their own account via the admin interface

## Attack demo resources

The `attacks/` folder contains simulated attacker pages used to demonstrate real CSRF payloads and attacker tactics.

Each page is designed around a specific vulnerable endpoint in the app and shows how an unsafe POST endpoint can be abused when the victim is already authenticated.

Detailed attack descriptions:

- `1. Zero click.html`
  - Attack type: hidden auto-submit CSRF form
  - Target: `POST /tasks/1/edit`
  - Behavior: when a victim opens the page, JavaScript auto-submits a form with hidden fields to silently update task #1. The page uses an invisible target iframe so the user never sees the request.
  - Impact: silently changes task title, description, status, and deadline without user awareness.
  - Why it works in the vulnerable version: the endpoint accepts POST edits without any CSRF token, and the browser automatically sends the victim's session cookie.

- `2. Q4_archiver.html`
  - Attack type: multi-request CSRF batch edit
  - Target: repeated `POST /tasks/{id}/edit` requests
  - Behavior: presents a fake “Q4 archive” UI, then submits several hidden edit forms in sequence to mark multiple tasks as completed and lock them for audit.
  - Impact: multiple user-owned tasks can be overwritten or coerced into a final state in one visit.
  - Why it works in the vulnerable version: the task edit endpoints are trusted based on session cookie alone, with no CSRF protection.

- `3. Data purge.html`
  - Attack type: automated delete CSRF flood
  - Target: repeated `POST /tasks/{id}/delete` requests for task IDs 1–20
  - Behavior: once the victim clicks the fake button, the page loops through task IDs and submits hidden delete forms to a hidden iframe.
  - Impact: if the victim owns any of those tasks, they will be deleted without intent.
  - Why it works in the vulnerable version: the delete endpoint accepts POST requests with session cookies and performs ownership checks only after the request arrives.

- `4. TaskAI Optimize.html`
  - Attack type: hidden fetch-based admin account creation
  - Target: `POST /admin/users/create`
  - Behavior: a malicious, branded page uses `fetch()` with `credentials: 'include'` to create a new admin user from the victim's authenticated session.
  - Impact: can silently introduce a backdoor admin account that the attacker later uses to escalate privileges.
  - Why it works in the vulnerable version: the admin creation endpoint accepted POSTs with unvalidated CSRF context, and the app originally allowed role values from form data.

These pages are kept for demonstration purposes; in the secure branch they highlight the exact attacks that should be prevented by CSRF tokens and cookie defenses.


## Notes for reviewers

- The vulnerable branch is `main_vulnerable`, which contains the same app with CSRF weaknesses preserved.

## Useful commands

- `python app/app.py` — start the Flask application
- `git branch --show-current` — confirm you are on `secure`

---

If you want to evaluate the attack payloads, open the files in `attacks/` in a browser and compare their behavior against this secure branch and the vulnerable branch.