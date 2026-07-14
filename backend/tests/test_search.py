def test_search_entity_by_value(client, auth_headers):
    resp = client.get("/api/v1/search?value=98", headers=auth_headers)
    assert resp.status_code == 200
    body = resp.json()
    assert body["query"] == "98"
    assert isinstance(body["results"], list)


def test_search_entity_type_filter(client, auth_headers):
    resp = client.get("/api/v1/search?value=98&entity_type=Phone", headers=auth_headers)
    assert resp.status_code == 200
    for result in resp.json()["results"]:
        assert result["entity_type"] == "Phone"


def test_search_value_too_short_rejected(client, auth_headers):
    resp = client.get("/api/v1/search?value=1", headers=auth_headers)
    assert resp.status_code == 422


def test_search_by_fir_found(client, auth_headers):
    case = client.get("/api/v1/cases?limit=1", headers=auth_headers).json()["items"][0]
    resp = client.get(f"/api/v1/search/fir/{case['fir_number']}", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["case_id"] == case["case_id"]


def test_search_by_fir_not_found(client, auth_headers):
    resp = client.get("/api/v1/search/fir/FIR_DOES_NOT_EXIST", headers=auth_headers)
    assert resp.status_code == 404
