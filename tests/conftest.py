import os

# Must be set before the app is imported.
os.environ["JWT_SECRET_KEY"] = "test-secret-key-for-velocity-tests-0123456789abcdef"
os.environ["DATABASE_URL"] = "sqlite://"

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402
from sqlalchemy import create_engine  # noqa: E402
from sqlalchemy.orm import sessionmaker  # noqa: E402
from sqlalchemy.pool import StaticPool  # noqa: E402

from app.main import app  # noqa: E402
from app.db.database import Base, get_db  # noqa: E402
from app.db.seed import seed_database  # noqa: E402


@pytest.fixture()
def session_factory():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    Base.metadata.create_all(engine)
    factory = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    with factory() as db:
        seed_database(db)
    yield factory
    engine.dispose()


@pytest.fixture()
def client(session_factory):
    def override_get_db():
        db = session_factory()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


def make_user(client, username="arya", password="password123"):
    email = f"{username}@example.com"
    r = client.post("/api/auth/register", json={"email": email, "username": username, "password": password})
    assert r.status_code == 201, r.text
    r = client.post("/api/auth/login", json={"email": email, "password": password})
    assert r.status_code == 200, r.text
    return {"Authorization": f"Bearer {r.json()['access_token']}"}


@pytest.fixture()
def auth_headers(client):
    return make_user(client, "arya")


@pytest.fixture()
def other_headers(client):
    return make_user(client, "bran")


@pytest.fixture()
def ids(client):
    """Map of option name -> id per category, read from the API."""
    opts = client.get("/api/options").json()
    result = {key: {item["name"]: item["id"] for item in items} for key, items in opts.items()}
    result["cars"] = {c["name"]: c["id"] for c in client.get("/api/cars").json()}
    return result


@pytest.fixture()
def payload(ids):
    """The full scenario build: Porsche 911 GT3 RS + Weissach Power + Weissach Package + Active DRS Aero."""
    return {
        "car_id": ids["cars"]["Porsche 911 GT3 RS"],
        "paint_id": ids["paints"]["Obsidian Black"],
        "wheel_id": ids["wheels"]["Carbon"],
        "caliper_id": ids["calipers"]["Red"],
        "interior_material_id": ids["interior_materials"]["Alcantara"],
        "interior_color_id": ids["interior_colors"]["Black"],
        "seat_type_id": ids["seat_types"]["Racing"],
        "engine_id": ids["engines"]["4.0L Flat-Six Weissach Power Spec"],
        "performance_package_id": ids["performance_packages"]["Weissach Package"],
        "aero_package_id": ids["aero_packages"]["Active DRS Aero Package"],
        "name": "Black Beast",
    }
