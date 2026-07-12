# Backend (FastAPI)

Not yet implemented. Planned structure:
- app/main.py — FastAPI entrypoint
- app/db/ — SQLAlchemy engine/session
- app/models/ — ORM models (one per table)
- app/schemas/ — Pydantic request/response models
- app/api/routes/ — cases, citizens, search, similar-cases, network, auth, audit, chat
- app/services/ — search_service, similarity_service, audit_service, nlp_service
- app/core/ — security.py (JWT/auth), rbac.py (role permission checks)

Depends on dataset/seed/schema.sql being loaded first.
