import jwt

from app.core.config import settings
from app.core.security import hash_password, verify_password

REG = {"email": "user@example.com", "username": "arya", "password": "password123"}


def test_register_successful(client):
    r = client.post("/api/auth/register", json=REG)
    assert r.status_code == 201
    body = r.json()
    assert body["email"] == "user@example.com" and body["username"] == "arya"
    assert "password" not in body and "hashed_password" not in body


def test_duplicate_email_rejected(client):
    client.post("/api/auth/register", json=REG)
    r = client.post("/api/auth/register", json={**REG, "username": "other"})
    assert r.status_code == 409


def test_duplicate_username_rejected(client):
    client.post("/api/auth/register", json=REG)
    r = client.post("/api/auth/register", json={**REG, "email": "other@example.com"})
    assert r.status_code == 409


def test_short_password_rejected(client):
    r = client.post("/api/auth/register", json={**REG, "password": "short"})
    assert r.status_code == 422


def test_invalid_email_rejected(client):
    r = client.post("/api/auth/register", json={**REG, "email": "not-an-email"})
    assert r.status_code == 422


def test_login_successful(client):
    client.post("/api/auth/register", json=REG)
    r = client.post("/api/auth/login", json={"email": REG["email"], "password": REG["password"]})
    assert r.status_code == 200
    body = r.json()
    assert body["token_type"] == "bearer" and body["access_token"]
    assert body["user"]["username"] == "arya"
    assert "hashed_password" not in body["user"]


def test_incorrect_password_rejected(client):
    client.post("/api/auth/register", json=REG)
    r = client.post("/api/auth/login", json={"email": REG["email"], "password": "wrongpassword"})
    assert r.status_code == 401


def test_unknown_user_rejected(client):
    r = client.post("/api/auth/login", json={"email": "nobody@example.com", "password": "password123"})
    assert r.status_code == 401


def test_me_without_token_rejected(client):
    assert client.get("/api/auth/me").status_code == 401


def test_me_with_invalid_token_rejected(client):
    r = client.get("/api/auth/me", headers={"Authorization": "Bearer garbage"})
    assert r.status_code == 401


def test_me_with_expired_token_rejected(client):
    token = jwt.encode({"sub": "1", "exp": 1}, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    r = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 401


def test_me_works(client, auth_headers):
    r = client.get("/api/auth/me", headers=auth_headers)
    assert r.status_code == 200
    assert r.json()["username"] == "arya"


def test_password_is_hashed():
    hashed = hash_password("password123")
    assert hashed != "password123"
    assert verify_password("password123", hashed)
    assert not verify_password("nope-nope", hashed)
