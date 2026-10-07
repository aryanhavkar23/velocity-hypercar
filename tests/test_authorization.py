def _build(client, headers, payload):
    return client.post("/api/configurations", json=payload, headers=headers).json()


def test_user_cannot_view_others_build(client, auth_headers, other_headers, payload):
    build = _build(client, auth_headers, payload)
    r = client.get(f"/api/configurations/{build['id']}", headers=other_headers)
    assert r.status_code == 403
    assert r.json() == {"detail": "Configuration does not belong to this user"}


def test_user_cannot_edit_others_build(client, auth_headers, other_headers, payload):
    build = _build(client, auth_headers, payload)
    r = client.put(f"/api/configurations/{build['id']}", json={"name": "Hacked"}, headers=other_headers)
    assert r.status_code == 403
    unchanged = client.get(f"/api/configurations/{build['id']}", headers=auth_headers).json()
    assert unchanged["name"] == "Black Beast"


def test_user_cannot_delete_others_build(client, auth_headers, other_headers, payload):
    build = _build(client, auth_headers, payload)
    assert client.delete(f"/api/configurations/{build['id']}", headers=other_headers).status_code == 403
    assert client.get(f"/api/configurations/{build['id']}", headers=auth_headers).status_code == 200


def test_garage_is_private(client, auth_headers, other_headers, payload):
    _build(client, auth_headers, payload)
    assert len(client.get("/api/garage", headers=auth_headers).json()["builds"]) == 1
    assert client.get("/api/garage", headers=other_headers).json()["builds"] == []
    assert client.get("/api/configurations", headers=other_headers).json() == []


def test_update_delete_require_auth(client, auth_headers, payload):
    build = _build(client, auth_headers, payload)
    assert client.put(f"/api/configurations/{build['id']}", json={"name": "x"}).status_code == 401
    assert client.delete(f"/api/configurations/{build['id']}").status_code == 401
