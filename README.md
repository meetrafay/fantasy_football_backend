# Fantasy Football Backend

A Django-based backend for a fantasy football application. This repository contains a Django project (fantasy_football_backend) and several app packages that implement core domain functionality (users, teams, transactions, transfers). The project exposes a REST API and includes standard Django management entrypoints.

This README focuses on development and Docker-based local setup.

Important files
- [manage.py](manage.py)
- [Dockerfile](Dockerfile)
- [docker-compose.yml](docker-compose.yml)
- [requirements.txt](requirements.txt)
- [.env.example](.env.example)
- Django settings: [`fantasy_football_backend.settings`](fantasy_football_backend/settings.py)

Quick setup (local, without Docker)
1. Create and activate a virtualenv:
   python -m venv .venv
   source .venv/bin/activate
2. Install dependencies:
   pip install -r requirements.txt
3. Copy environment example and edit:
   cp .env.example .env
   Edit `.env` and set DB_NAME/DB_USER/DB_PASS/DB_HOST/DB_PORT or use local defaults.
4. Apply migrations:
   python manage.py migrate
5. Run dev server:
   python manage.py runserver

Docker (recommended for consistent dev DB)
1. Copy and update environment:
   cp .env.example .env
   Edit `.env` (set DB_NAME/DB_USER/DB_PASS if desired). The compose file sets DB host to `db`.
2. Build and start services:
   docker-compose up --build -d
   - The compose file uses the development server (Django runserver) for the `web` service: see [docker-compose.yml](docker-compose.yml) and [Dockerfile](Dockerfile).
3. View logs:
   docker-compose logs -f web

Run tests (inside container)
- Run full test suite in the container:
  docker-compose run --rm web python manage.py test
- Or run tests in a running container:
  docker-compose exec web python manage.py test
- Run a single test case (faster):
  docker-compose run --rm web python manage.py test transfers.tests.TransfersIntegrationTestCase
Test files include:
- [users/tests.py](users/tests.py)
- [teams/tests.py](teams/tests.py)
- [transfers/tests.py](transfers/tests.py)
- [transactions/tests.py](transactions/tests.py)

Notes about services and tests
- Team creation: [`teams.services.team_creation.TeamCreationService.get_or_create_team_for_user`](teams/services/team_creation.py)
- Transfer listing/purchase: [`transfers.services.transfer_listing.TransferListingService`](transfers/services/transfer_listing.py) and [`transfers.services.player_purchase.TransferPurchaseService`](transfers/services/player_purchase.py)
- Transaction records: [`transactions.services.transaction.TransactionService`](transactions/services/transaction.py)

Troubleshooting
- If the web container cannot connect to the DB during startup, check `.env` values and `docker-compose logs db`.
- To re-create volumes (Postgres data) during development:
  docker-compose down -v && docker-compose up --build
- If migrations
