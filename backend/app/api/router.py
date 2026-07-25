"""
Aggregates every resource router into a single `api_router` so main.py
only has one include_router() call. Router file name = URL prefix = model
file name stays true per-file (see routes/*.py); this module just collects
them.
"""
from fastapi import APIRouter

from app.api.routes import (
    analytics,
    audit,
    auth,
    cases,
    chat,
    dashboard,
    officers,
    persons,
    search,
    stations,
    users,
)

api_router = APIRouter()

for _router in (
    auth.router,
    cases.router,
    persons.router,
    search.router,
    officers.router,
    stations.router,
    analytics.router,
    dashboard.router,
    chat.router,
    audit.router,
    users.router,
):
    api_router.include_router(_router)
