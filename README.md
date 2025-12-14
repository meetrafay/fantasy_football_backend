# Fantasy Football Backend

A Django-based backend for a fantasy football application. This repository contains a Django project (fantasy_football_backend) and several app packages that implement core domain functionality (users, teams, transactions, transfers). The project exposes an API (REST endpoints are expected) and includes standard Django management entrypoints (manage.py).

This README is tailored to this repository and explains the project, how to get it running, and where to find the API endpoints.

## Table of contents
- [Project overview](#project-overview)
- [Repository structure](#repository-structure)
- [Requirements](#requirements)
- [Quick setup (local)](#quick-setup-local)
- [Environment variables](#environment-variables)
- [Database & migrations](#database--migrations)
- [Run the server](#run-the-server)
- [Testing](#testing)
- [APIs (high level)](#apis-high-level)
- [Finding exact routes](#finding-exact-routes)
- [Common management commands](#common-management-commands)


## Project overview
This is the backend service for a fantasy football application, implemented in Django. It provides user management, team management, and transaction/transfer handling. The Django project root is `fantasy_football_backend/` and the project entrypoint is `manage.py`.

Primary apps present in the repository:
- users — user accounts, auth, profiles
- teams — team creation and roster endpoints
- transactions — logs/actions for trades or other financial/transactional operations
- transfers — player transfer workflows

The repository includes:
- `manage.py` — Django CLI entrypoint
- `fantasy_football_backend/` — Django project (settings, urls, wsgi/asgi)
- `users/`, `teams/`, `transactions/`, `transfers/` — app packages
- `.env.example` — example environment variables

## Requirements
- Python 3.8+ (3.10+ recommended)
- pip
- Virtual environment tooling (venv, virtualenv)
- A database supported by Django (PostgreSQL recommended for production)
- Optional: Redis (for caching, channels) if project uses it

There may be a `requirements.txt` in the repository — present install packages from it:
- Django
- djangorestframework (if REST API is used)
- python-dotenv or django-environ (if environment variables are read from .env)

## Quick setup (local)
1. Clone the repository:
   git clone https://github.com/meetrafay/fantasy_football_backend.git
   cd fantasy_football_backend

2. Create and activate a virtual environment:
   python -m venv .venv
   source .venv/bin/activate    # macOS / Linux
   .venv\Scripts\activate       # Windows (PowerShell/CMD)

3. Install dependencies:
   - If `requirements.txt` exists:
     pip install -r requirements.txt
   - Otherwise install core packages:
     pip install Django djangorestframework python-dotenv

4. Copy environment example and edit:
   cp .env.example .env
   Edit `.env` and set database credentials and any other required secrets.

5. Apply database migrations (see next section for DB setup).

## Environment variables
There is an `.env.example` file in the repo root. Typical variables you should set in `.env`:
- SECRET_KEY (Django secret)
- DEBUG (True/False)
- DATABASE_URL or standard Django DB settings (DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT)
- Any third-party API keys or service URLs used by the project

Do not commit `.env` to version control.

## Database & migrations
1. Configure your database in `.env` or in `fantasy_football_backend/settings.py`.
2. Create the database in your DB server (Postgres recommended).
3. Run Django migrations:
   python manage.py migrate

4. (Optional) Create a superuser:
   python manage.py createsuperuser

## Run the server
Start the development server:
python manage.py runserver

By default Django listens on http://127.0.0.1:8000. Use `--settings` environment variable or DJANGO_SETTINGS_MODULE if you need to point to a different config.

## Testing
Run the Django test suite:
python manage.py test

Ensure your test database config is valid (Django creates a test DB automatically when running tests).

## APIs (high level)
The project organizes functionality into the following apps, which normally map to API endpoints:

- /admin/  
  Django admin interface (requires superuser).

- /users/ or /api/users/  
  Endpoints for user registration, login, profile management.

- /teams/ or /api/teams/  
  Create/list teams, manage rosters.

- /transactions/ or /api/transactions/  
  Create/list transactions associated with teams or players.

- /transfers/ or /api/transfers/  
  Endpoints to handle player transfers between teams.

Note: The exact URL prefixes and available endpoints are defined in `fantasy_football_backend/urls.py` and in each app's `urls.py`. Use the section below to find precise routes.

Example API request (replace path with actual path from your urls):
curl -X GET "http://127.0.0.1:8000/api/teams/" -H "Accept: application/json"

If the project uses token authentication or JWT, include the Authorization header:
-H "Authorization: Bearer <token>"

## Finding exact routes
To see the registered routes in this Django project:
- Inspect `fantasy_football_backend/urls.py` and each app's `urls.py` (users, teams, transactions, transfers).
- If you have `django-extensions` installed, you can run:
  python manage.py show_urls
- Start the dev server and navigate to `/` or API docs (if swagger/redoc is configured).

## Common management commands
- python manage.py migrate — apply migrations
- python manage.py makemigrations <app> — create a new migration for an app
- python manage.py createsuperuser — create admin user
- python manage.py collectstatic — collect static files (for production)
- python manage.py test — run tests
- python manage.py runserver — start dev server

## END
