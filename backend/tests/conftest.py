"""
Fixtures assume DATABASE_URL (from .env / environment) points at a Postgres
instance with dataset/seed/schema.sql loaded and at least one row in
`users` with a known hashed_password — see backend/README.md "Running
tests" for the one-time setup. These are integration tests against a real
DB on purpose: the routes are thin, and the SQL (joins, RBAC scoping,
full-text search) is where bugs actually hide.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select

from app.core.security import hash_password
from app.db.session import SessionLocal
from app.main import app
from app.models.user import User

TEST_USERNAME = "pytest_admin"
TEST_PASSWORD = "pytest-pass-123"


@pytest.fixture(scope="session", autouse=True)
def ensure_test_user():
    """Creates (or updates) a throwaway Admin-role user for the test run."""
    db = SessionLocal()
    try:
        user = db.execute(select(User).where(User.username == TEST_USERNAME)).scalar_one_or_none()
        if user is None:
            user = User(
                user_id="USRPYTEST1",
                username=TEST_USERNAME,
                role_id="ROLE01",  # Admin — see dataset/processed/roles.csv
                status="Active",
            )
            db.add(user)
        user.hashed_password = hash_password(TEST_PASSWORD)
        user.status = "Active"
        db.commit()
    finally:
        db.close()
    yield


@pytest.fixture()
def client():
    return TestClient(app)


@pytest.fixture()
def auth_headers(client):
    resp = client.post(
        "/api/v1/auth/login",
        json={"username": TEST_USERNAME, "password": TEST_PASSWORD},
    )
    assert resp.status_code == 200, resp.text
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
