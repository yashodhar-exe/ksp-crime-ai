def test_login_success(client, auth_headers):
    assert "Authorization" in auth_headers


def test_login_wrong_password(client):
    resp = client.post(
        "/api/v1/auth/login",
        json={"username": "pytest_admin", "password": "wrong-password"},
    )
    assert resp.status_code == 401


def test_login_unknown_user(client):
    resp = client.post(
        "/api/v1/auth/login",
        json={"username": "no_such_user", "password": "whatever"},
    )
    assert resp.status_code == 401


def test_protected_route_requires_token(client):
    resp = client.get("/api/v1/cases")
    assert resp.status_code == 401


def test_refresh_flow(client):
    login = client.post(
        "/api/v1/auth/login",
        json={"username": "pytest_admin", "password": "pytest-pass-123"},
    )
    refresh_token = login.json()["refresh_token"]
    resp = client.post("/api/v1/auth/refresh", json={"refresh_token": refresh_token})
    assert resp.status_code == 200
    assert "access_token" in resp.json()


def test_logout(client, auth_headers):
    resp = client.post("/api/v1/auth/logout", headers=auth_headers)
    assert resp.status_code == 204
