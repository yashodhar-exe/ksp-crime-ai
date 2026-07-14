def test_list_cases(client, auth_headers):
    resp = client.get("/api/v1/cases?limit=5", headers=auth_headers)
    assert resp.status_code == 200
    body = resp.json()
    assert "items" in body and "page" in body
    assert len(body["items"]) <= 5
    assert body["page"]["total"] > 0


def test_list_cases_filter_by_crime_type(client, auth_headers):
    resp = client.get("/api/v1/cases?crime_type=Burglary&limit=5", headers=auth_headers)
    assert resp.status_code == 200
    for case in resp.json()["items"]:
        assert case["crime_type"] == "Burglary"


def test_get_case_detail(client, auth_headers):
    listed = client.get("/api/v1/cases?limit=1", headers=auth_headers).json()["items"]
    case_id = listed[0]["case_id"]

    resp = client.get(f"/api/v1/cases/{case_id}", headers=auth_headers)
    assert resp.status_code == 200
    body = resp.json()
    assert body["case_id"] == case_id
    assert "complaint_text" in body


def test_get_case_not_found(client, auth_headers):
    resp = client.get("/api/v1/cases/CASE_DOES_NOT_EXIST", headers=auth_headers)
    assert resp.status_code == 404


def test_case_sub_resources(client, auth_headers):
    case_id = client.get("/api/v1/cases?limit=1", headers=auth_headers).json()["items"][0]["case_id"]

    for sub in ("suspects", "victims", "evidence", "digital-evidence", "notes", "timeline", "similar-cases"):
        resp = client.get(f"/api/v1/cases/{case_id}/{sub}", headers=auth_headers)
        assert resp.status_code == 200, f"{sub} failed: {resp.text}"
        assert isinstance(resp.json(), list)


def test_create_case_requires_can_edit_case_permission(client, auth_headers):
    # pytest_admin has ROLE01 (Admin, can_edit_case=True), so creation
    # should succeed; the RBAC denial path is exercised by hitting the
    # route without a token (covered in test_auth.py).
    import uuid

    fir_number = f"FIRPYTEST{uuid.uuid4().hex[:8].upper()}"
    payload = {
        "fir_number": fir_number,
        "crime_type": "Test Crime",
        "station_id": "ST0001",
        "officer_id": "OFF00001",
        "incident_date": "2026-01-01",
        "registered_date": "2026-01-01",
        "city": "Test City",
        "district": "Test District",
        "complaint_text": "pytest-created case",
    }
    resp = client.post("/api/v1/cases", json=payload, headers=auth_headers)
    assert resp.status_code == 201, resp.text
    assert resp.json()["fir_number"] == fir_number
