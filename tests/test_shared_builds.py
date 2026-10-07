import json


def _build(client, headers, payload):
    return client.post("/api/configurations", json=payload, headers=headers).json()


def test_public_build_id_works_without_auth(client, auth_headers, payload):
    build = _build(client, auth_headers, payload)
    r = client.get(f"/api/configurations/build/{build['build_id']}")  # no headers
    assert r.status_code == 200
    body = r.json()
    assert body["build_id"] == build["build_id"] and body["name"] == "Black Beast"
    assert body["car"]["name"] == "Porsche 911 GT3 RS"
    assert body["exterior"] == build["exterior"] and body["interior"] == build["interior"]
    assert body["performance"] == build["performance"] and body["pricing"] == build["pricing"]


def test_public_build_hides_private_user_info(client, auth_headers, payload):
    build = _build(client, auth_headers, payload)
    body = client.get(f"/api/configurations/build/{build['build_id']}").json()
    text = json.dumps(body).lower()
    for secret in ("arya", "@example.com", "user_id", "email", "password", "hashed"):
        assert secret not in text
    assert "user" not in body and "id" not in body


def test_build_id_lookup_is_case_insensitive(client, auth_headers, payload):
    build = _build(client, auth_headers, payload)
    r = client.get(f"/api/configurations/build/{build['build_id'].lower()}")
    assert r.status_code == 200


def test_unknown_build_id_404(client):
    assert client.get("/api/configurations/build/VX-00000").status_code == 404


def test_malformed_build_id_400(client):
    for bad in ("hello", "VX-123", "VX-ZZZZZ", "AB-12345", "VX-123456"):
        assert client.get(f"/api/configurations/build/{bad}").status_code == 400, bad


def test_full_mvp_flow(client, payload):
    reg = {"email": "flow@example.com", "username": "flow", "password": "password123"}
    assert client.post("/api/auth/register", json=reg).status_code == 201
    token = client.post("/api/auth/login", json={"email": reg["email"], "password": reg["password"]}).json()["access_token"]
    h = {"Authorization": f"Bearer {token}"}
    assert client.get("/api/auth/me", headers=h).json()["username"] == "flow"
    created = client.post("/api/configurations", json=payload, headers=h)
    assert created.status_code == 201
    cid, bid = created.json()["id"], created.json()["build_id"]
    assert client.get("/api/garage", headers=h).json()["builds"][0]["build_id"] == bid
    assert client.put(f"/api/configurations/{cid}", json={"name": "Renamed"}, headers=h).status_code == 200
    assert client.get(f"/api/configurations/build/{bid}").json()["name"] == "Renamed"
    assert client.delete(f"/api/configurations/{cid}", headers=h).status_code == 200
    assert client.get("/api/garage", headers=h).json()["builds"] == []
