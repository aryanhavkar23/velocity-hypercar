EXPECTED_CARS = [
    "Porsche 911 GT3 RS",
    "Suzuki Swift",
]


def test_list_cars(client):
    r = client.get("/api/cars")
    assert r.status_code == 200
    names = [c["name"] for c in r.json()]
    assert names == EXPECTED_CARS
    assert len(names) == 2


def test_get_car(client):
    car = client.get("/api/cars/1").json()
    assert car["name"] == "Porsche 911 GT3 RS"
    assert car["base_price"] == 35_000_000
    assert car["horsepower"] == 525 and car["top_speed"] == 296
    assert car["acceleration"] == 3.2
    assert car["handling"] == 98 and car["braking"] == 97


def test_all_cars_retrieval_and_specs(client):
    cars = client.get("/api/cars").json()
    assert len(cars) == 2
    for c in cars:
        assert c["name"] in EXPECTED_CARS
        assert c["base_price"] > 0
        assert c["horsepower"] > 0
        assert c["top_speed"] > 0
        assert c["acceleration"] > 0
        assert 0 <= c["handling"] <= 100
        assert 0 <= c["braking"] <= 100
        assert c["image_url"].startswith("/assets/")
        assert len(c["description"]) > 0

        # Verify individual endpoint works
        single = client.get(f"/api/cars/{c['id']}").json()
        assert single["name"] == c["name"]
        assert single["slug"] == c["slug"]


def test_old_fictional_cars_not_active(client):
    names = [c["name"] for c in client.get("/api/cars").json()]
    for fictional in ("Vortex X1", "Apex R", "Phantom GT"):
        assert fictional not in names


def test_invalid_car_returns_404(client):
    assert client.get("/api/cars/9999").status_code == 404


def test_inactive_car_hidden(client, session_factory):
    from app.models import Car
    with session_factory() as db:
        db.get(Car, 1).is_active = False
        db.commit()
    active_names = [c["name"] for c in client.get("/api/cars").json()]
    assert "Porsche 911 GT3 RS" not in active_names
    assert len(active_names) == 1
    assert client.get("/api/cars/1").status_code == 404


def test_options_load(client):
    body = client.get("/api/options").json()
    counts = {k: len(v) for k, v in body.items()}
    assert counts == {
        "paints": 5, "wheels": 4, "calipers": 4, "interior_materials": 3, "interior_colors": 4,
        "seat_types": 3, "engines": 4, "performance_packages": 4, "aero_packages": 4,
    }


def test_car_filtered_options(client, ids):
    swift_id = ids["cars"]["Suzuki Swift"]
    swift_opts = client.get(f"/api/options?car_id={swift_id}").json()
    engine_names = [e["name"] for e in swift_opts["engines"]]
    assert "1.2L Z-Series Three-Cylinder" in engine_names
    assert "4.0L Naturally Aspirated Flat-Six" not in engine_names


def test_inactive_options_excluded(client, session_factory):
    from app.models import Paint
    with session_factory() as db:
        paint = db.query(Paint).filter_by(name="Neon Green").one()
        paint.is_active = False
        db.commit()
    names = [p["name"] for p in client.get("/api/options").json()["paints"]]
    assert "Neon Green" not in names and len(names) == 4
    assert "Neon Green" not in [p["name"] for p in client.get("/api/options/paints").json()]


def test_individual_option_endpoints(client):
    for path, n in [("paints", 5), ("wheels", 4), ("calipers", 4), ("interior-materials", 3),
                    ("interior-colors", 4), ("seat-types", 3), ("engines", 4),
                    ("performance-packages", 4), ("aero-packages", 4)]:
        r = client.get(f"/api/options/{path}")
        assert r.status_code == 200 and len(r.json()) == n, path


def test_seed_is_idempotent(client, session_factory):
    from app.db.seed import seed_database
    from app.models import Car, Engine
    with session_factory() as db:
        assert seed_database(db) == 0
        assert seed_database(db) == 0
        assert db.query(Car).count() == 2 and db.query(Engine).count() == 4


def test_system_endpoints(client):
    assert client.get("/health").json() == {"status": "ok", "service": "velocity-backend"}
    root = client.get("/").json()
    assert root["docs"] == "/docs" and root["version"] == "1.0.0"
