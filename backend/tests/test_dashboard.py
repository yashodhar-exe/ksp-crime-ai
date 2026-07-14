def test_dashboard_summary(client, auth_headers):
    resp = client.get("/api/v1/dashboard/summary", headers=auth_headers)
    assert resp.status_code == 200
    body = resp.json()
    assert body["total_cases"] > 0
    assert body["total_citizens"] > 0


def test_dashboard_stats(client, auth_headers):
    resp = client.get("/api/v1/dashboard/stats", headers=auth_headers)
    assert resp.status_code == 200
    body = resp.json()
    assert len(body["by_status"]) > 0
    assert len(body["by_crime_type"]) > 0


def test_dashboard_recent(client, auth_headers):
    resp = client.get("/api/v1/dashboard/recent?limit=3", headers=auth_headers)
    assert resp.status_code == 200
    assert len(resp.json()["cases"]) <= 3


def test_dashboard_activity(client, auth_headers):
    resp = client.get("/api/v1/dashboard/activity?limit=5", headers=auth_headers)
    assert resp.status_code == 200
    assert isinstance(resp.json()["entries"], list)


def test_dashboard_requires_auth(client):
    resp = client.get("/api/v1/dashboard/summary")
    assert resp.status_code == 401
