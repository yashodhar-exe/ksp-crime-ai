from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.api.router import api_router
from app.config import settings
from app.db.session import engine

app = FastAPI(title=settings.APP_NAME, version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_PREFIX)


# --- Unversioned health check, for load balancers / simple uptime pings ---
@app.get("/health", tags=["health"])
def health_check() -> dict[str, str]:
    return {"status": "ok"}


# --- Versioned deployment probes ---
@app.get(f"{settings.API_V1_PREFIX}/health", tags=["health"])
def health_check_v1() -> dict[str, str]:
    return {"status": "ok"}


@app.get(f"{settings.API_V1_PREFIX}/version", tags=["health"])
def version() -> dict[str, str]:
    return {"app": settings.APP_NAME, "version": app.version, "env": settings.ENV}


@app.get(f"{settings.API_V1_PREFIX}/liveness", tags=["health"])
def liveness() -> dict[str, str]:
    """Process is up and serving requests — no dependency checks."""
    return {"status": "alive"}


@app.get(f"{settings.API_V1_PREFIX}/readiness", tags=["health"])
def readiness() -> dict[str, str]:
    """Process can actually serve traffic — verifies the DB connection."""
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    return {"status": "ready"}
