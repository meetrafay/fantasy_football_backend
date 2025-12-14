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
- If migrations fail repeatedly, run:
  docker-compose run --rm web python manage.py migrate --traceback

Production notes
- Current Docker setup uses Django development server (suitable for local development only). For production use a WSGI server (e.g., gunicorn) and a reverse proxy (nginx). See [Dockerfile](Dockerfile) and [docker-compose.yml](docker-compose.yml) to switch servers.

References
- Project settings: [`fantasy_football_backend.settings`](fantasy_football_backend/settings.py)
- App routes (see): [fantasy_football_backend/urls.py](fantasy_football_backend/urls.py)
- API test coverage: [users/tests.py](users/tests.py), [teams/tests.py](teams/tests.py), [transfers/tests.py](transfers/tests.py), [transactions/tests.py](transactions/tests.py)
- Requirements: [requirements.txt](requirements.txt)

API Endpoints
- User signup (creates User + Profile + Team)
  - POST /api/user/signup/
  - View: [`users.views.signup.SignupView`](users/views/signup.py)
  - Example:
    curl -X POST http://localhost:8000/api/user/signup/ -H "Content-Type: application/json" \
      -d '{"email":"alice@example.com","password":"strongpass","username":"Alice","country":"Wonderland"}'

- User login (returns JWT tokens)
  - POST /api/user/login/
  - View: [`users.views.login.LoginView`](users/views/login.py)
  - Utility: [`users.utils.create_token`](users/utils.py)
  - Example:
    curl -X POST http://localhost:8000/api/user/login/ -H "Content-Type: application/json" \
      -d '{"email":"alice@example.com","password":"strongpass"}'

- Get current user's team
  - GET /api/my/team/
  - View: [`teams.views.team_detail.MyTeamDetailView`](teams/views/team_detail.py)

- List a player for sale
  - POST /api/list/player/
  - View: [`transfers.views.player_list.ListPlayerForSaleView`](transfers/views/player_list.py)
  - Serializer/service: [`transfers.serializers.player_transfer_listing.ListPlayerSerializer`](transfers/serializers/player_transfer_listing.py), [`transfers.services.transfer_listing.TransferListingService`](transfers/services/transfer_listing.py)
  - Example (requires Authorization header with Bearer <access_token>):
    curl -X POST http://localhost:8000/api/list/player/ -H "Content-Type: application/json" \
      -H "Authorization: Bearer <ACCESS_TOKEN>" -d '{"player_id": 1, "price": 2500000}'

- View marketplace listings
  - GET /api/players/market/
  - View: [`transfers.views.players_market.MarketListingView`](transfers/views/players_market.py)
  - Serializer: [`transfers.serializers.players_market.TransferListingSerializer`](transfers/serializers/players_market.py)

- Buy a player
  - POST /api/buy/player/
  - View: [`transfers.views.buy_player.BuyPlayerView`](transfers/views/buy_player.py)
  - Serializer/service: [`transfers.serializers.buy_player.BuyPlayerSerializer`](transfers/serializers/buy_player.py), [`transfers.services.player_purchase.TransferPurchaseService`](transfers/services/player_purchase.py)
  - Example:
    curl -X POST http://localhost:8000/api/buy/player/ -H "Content-Type: application/json" \
      -H "Authorization: Bearer <ACCESS_TOKEN>" -d '{"listing_id": 1}'

- List all transactions
  - GET /api/all/transactions/
  - View: [`transactions.views.all_transactions.TransactionListView`](transactions/views/all_transactions.py)

- List my transactions
  - GET /api/my/transactions/
  - View: [`transactions.views.my_transactions.MyTransactionListView`](transactions/views/my_transactions.py)
  - Serializer: [`transactions.serializers.trasaction.TransactionSerializer`](transactions/serializers/trasaction.py)
  - Service: [`transactions.services.transaction.TransactionService`](transactions/services/transaction.py)

Notes
- All authenticated endpoints require a valid JWT access token in the Authorization header:
  Authorization: Bearer <ACCESS_TOKEN>
- Routes are relative to the API versioned root URL, e.g., `/api/v1/...`.
