# Backend (FastAPI)

Implements the route design in `docs/` (auth, cases, citizens, search,
officers, stations, network, analytics, chat, audit-logs, users) against
`dataset/seed/schema.sql`.

## Structure

- `app/main.py` — FastAPI entrypoint; mounts `app/api/router.py`'s `api_router` under `/api/v1`, plus health/version/readiness/liveness probes
- `app/api/router.py` — aggregates every resource router into one `api_router`
- `app/config.py` — settings, loaded from `.env`
- `app/db/` — SQLAlchemy engine/session (`session.py`) + declarative base (`base.py`)
- `app/models/` — one file per table, 1:1 with `schema.sql` (see note below)
- `app/schemas/` — Pydantic request/response models
- `app/api/deps.py` — `get_current_user`, `require_role()`
- `app/api/routes/` — one router per resource: auth, cases, citizens, search, officers, stations, network, analytics, dashboard, chat, audit, users
- `app/services/` — query/business logic (keeps routes thin)
- `app/core/security.py` — password hashing, JWT encode/decode
- `app/core/rbac.py` — permission checks against the `roles` table
- `alembic/` — schema migrations *on top of* `schema.sql`

## Health / deployment probes

- `GET /health` — unversioned, for load balancers
- `GET /api/v1/health` — same, under the API prefix
- `GET /api/v1/version` — app name/version/env
- `GET /api/v1/liveness` — process is up, no dependency checks
- `GET /api/v1/readiness` — verifies the DB connection is actually reachable

## Dashboard

`GET /api/v1/dashboard/{summary,stats,recent,activity}` composes existing
case/analytics/audit queries (no new tables) into the aggregated views a
frontend home screen needs. District-scoped the same way `/cases` is
(`core/rbac.scoped_district`); `activity` shows org-wide entries only to
roles with `can_view_all_districts`, otherwise just the caller's own.

## One addition beyond `schema.sql`

`schema.sql` models the seeded demo dataset, which has no login
credentials. `users.hashed_password` isn't a column there, so it's added
via `alembic/versions/0001_add_users_hashed_password.py`. Everything else
in `app/models/` matches `schema.sql` exactly — see the note in
`app/models/user.py`.

## Setup

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

cp ../.env.example .env   # then edit DATABASE_URL/JWT_SECRET as needed

# 1. Start Postgres and load the base schema + demo dataset (see root README)
docker compose up -d db
psql $DATABASE_URL -f ../dataset/seed/schema.sql
python ../dataset/seed/load_database.py

# 2. Apply the one migration on top of that (adds users.hashed_password)
alembic upgrade head

# 3. Give a demo user a password (schema.sql ships no credentials)
python -c "
from app.core.security import hash_password
print(hash_password('yourpassword'))
"
psql $DATABASE_URL -c "UPDATE users SET hashed_password='<hash from above>' WHERE user_id='USR0001';"

# 4. Run
uvicorn app.main:app --reload
```

API docs at `http://localhost:8000/docs` once running.

## Running tests

Tests run against a real Postgres with `schema.sql` + the dataset loaded
(they exercise actual joins, RBAC scoping, and full-text search rather
than mocking the DB). Point `DATABASE_URL` at that database, then:

```bash
pytest tests/ -v
```

`tests/conftest.py` creates/updates a throwaway `pytest_admin` user
(Admin role) for the run — it doesn't touch the rest of the seeded data.

## Notes

- Chat history (`/chat/history`, `/chat/export`) is stored in-process
  (`app/services/chat_store.py`) — fine for a demo/single-worker
  deployment; swap for a `chat_sessions`/`chat_messages` table for
  persistence across restarts or multiple workers.
- `/chat/query` falls back to Postgres full-text search over
  `cases.complaint_text` (the GIN index `schema.sql` already creates) when
  no LLM/vector DB is configured. Wire `app/services/nlp_service.py` into
  the `ai/rag` pipeline once that exists to upgrade it to real RAG.
- `similar-cases` uses a simple same-pattern / same-crime-type heuristic
  (`app/services/similarity_service.py`) — a stand-in for the "predictive
  analytics" scope note in the root README.
