import re

import pytest


def _create(client, headers, payload, **overrides):
    return client.post("/api/configurations", json={**payload, **overrides}, headers=headers)


def test_create_build(client, auth_headers, payload):
    r = _create(client, auth_headers, payload)
    assert r.status_code == 201, r.text
    body = r.json()
    assert body["name"] == "Black Beast"
    assert body["car"]["name"] == "Porsche 911 GT3 RS"
    assert body["exterior"]["paint"]["name"] == "Obsidian Black"
    assert body["exterior"]["paint"]["hex_code"] == "#080808"
    assert body["exterior"]["wheels"]["name"] == "Carbon"
    assert body["interior"]["seat"]["name"] == "Racing"
    assert body["performance"]["engine"]["name"] == "4.0L Flat-Six Weissach Power Spec"
    assert body["performance"]["package"]["name"] == "Weissach Package"
    assert body["performance"]["aero"]["name"] == "Active DRS Aero Package"
    p = body["pricing"]
    assert p["final_price"] == p["base_price"] + p["options_total"]


def test_build_id_format_and_uniqueness(client, auth_headers, payload):
    build_ids = [_create(client, auth_headers, payload).json()["build_id"] for _ in range(15)]
    assert all(re.fullmatch(r"VX-[0-9A-F]{5}", b) for b in build_ids)
    assert len(set(build_ids)) == 15


def test_client_price_and_stats_are_ignored(client, auth_headers, payload):
    honest = _create(client, auth_headers, payload).json()
    cheat = _create(client, auth_headers, payload, calculated_price=1, final_price=1,
                    horsepower=99999, stats={"horsepower": 99999}).json()
    assert cheat["pricing"] == honest["pricing"]
    assert cheat["performance"]["stats"] == honest["performance"]["stats"]


def test_create_requires_auth(client, payload):
    assert client.post("/api/configurations", json=payload).status_code == 401


@pytest.mark.parametrize("field", [
    "car_id", "paint_id", "wheel_id", "caliper_id", "interior_material_id", "interior_color_id",
    "seat_type_id", "engine_id", "performance_package_id", "aero_package_id",
])
def test_nonexistent_ids_rejected(client, auth_headers, payload, field):
    assert _create(client, auth_headers, payload, **{field: 9999}).status_code == 400


def test_negative_and_zero_ids_rejected(client, auth_headers, payload):
    assert _create(client, auth_headers, payload, engine_id=-1).status_code == 422
    assert _create(client, auth_headers, payload, paint_id=0).status_code == 422


def test_missing_field_rejected(client, auth_headers, payload):
    del payload["engine_id"]
    assert _create(client, auth_headers, payload).status_code == 422


def test_inactive_option_rejected(client, auth_headers, payload, session_factory):
    from app.models import Engine
    with session_factory() as db:
        db.get(Engine, payload["engine_id"]).is_active = False
        db.commit()
    r = _create(client, auth_headers, payload)
    assert r.status_code == 400 and "engine_id" in r.json()["detail"]


def test_inactive_car_rejected(client, auth_headers, payload, session_factory):
    from app.models import Car
    with session_factory() as db:
        db.get(Car, payload["car_id"]).is_active = False
        db.commit()
    assert _create(client, auth_headers, payload).status_code == 400


def test_saved_build_appears_in_garage(client, auth_headers, payload):
    created = _create(client, auth_headers, payload).json()
    garage = client.get("/api/garage", headers=auth_headers).json()
    assert len(garage["builds"]) == 1
    build = garage["builds"][0]
    assert build["build_id"] == created["build_id"]
    assert build["name"] == "Black Beast" and build["car"] == "Porsche 911 GT3 RS"
    assert build["price"] == created["pricing"]["final_price"]


def test_garage_requires_auth(client):
    assert client.get("/api/garage").status_code == 401


def test_list_and_get_configuration(client, auth_headers, payload):
    created = _create(client, auth_headers, payload).json()
    listing = client.get("/api/configurations", headers=auth_headers).json()
    assert [c["id"] for c in listing] == [created["id"]]
    one = client.get(f"/api/configurations/{created['id']}", headers=auth_headers)
    assert one.status_code == 200 and one.json() == created


def test_get_missing_configuration_404(client, auth_headers):
    assert client.get("/api/configurations/9999", headers=auth_headers).status_code == 404


def test_update_build_recalculates(client, auth_headers, payload, ids):
    created = _create(client, auth_headers, payload).json()
    r = client.put(
        f"/api/configurations/{created['id']}",
        json={"engine_id": ids["engines"]["4.0L Naturally Aspirated Flat-Six"],
              "performance_package_id": ids["performance_packages"]["Clubsport Package"],
              "aero_package_id": ids["aero_packages"]["Standard GT3 RS Aero"],
              "name": "Calm Beast",
              "calculated_price": 1},
        headers=auth_headers,
    )
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["name"] == "Calm Beast"
    assert body["build_id"] == created["build_id"]  # public ID stays stable
    assert body["performance"]["engine"]["name"] == "4.0L Naturally Aspirated Flat-Six"
    assert body["performance"]["stats"] == {
        "horsepower": 525, "top_speed": 296, "acceleration": 3.2, "handling": 98, "braking": 97,
    }
    # 450k + 25k + 350k + 250k = 1,075,000 (Carbon wheels, Red caliper, Alcantara, Racing seats)
    assert body["pricing"]["options_total"] == 1_075_000
    assert body["updated_at"] >= created["updated_at"]


def test_update_can_change_car(client, auth_headers, payload, ids):
    created = _create(client, auth_headers, payload).json()
    r = client.put(
        f"/api/configurations/{created['id']}",
        json={
            "car_id": ids["cars"]["Suzuki Swift"],
            "engine_id": ids["engines"]["1.2L Z-Series Three-Cylinder"],
            "performance_package_id": ids["performance_packages"]["Standard City Setup"],
            "aero_package_id": ids["aero_packages"]["Standard Bodywork"],
        },
        headers=auth_headers,
    )
    assert r.status_code == 200, r.text
    assert r.json()["car"]["name"] == "Suzuki Swift"
    assert r.json()["pricing"]["base_price"] == 849_000


def test_update_with_invalid_id_rejected_and_unchanged(client, auth_headers, payload):
    created = _create(client, auth_headers, payload).json()
    r = client.put(f"/api/configurations/{created['id']}", json={"paint_id": 9999}, headers=auth_headers)
    assert r.status_code == 400
    again = client.get(f"/api/configurations/{created['id']}", headers=auth_headers).json()
    assert again == created


def test_delete_build(client, auth_headers, payload):
    created = _create(client, auth_headers, payload).json()
    r = client.delete(f"/api/configurations/{created['id']}", headers=auth_headers)
    assert r.status_code == 200
    assert r.json() == {"message": "Configuration deleted successfully"}
    assert client.get(f"/api/configurations/{created['id']}", headers=auth_headers).status_code == 404
    assert client.get("/api/garage", headers=auth_headers).json()["builds"] == []
    assert client.get(f"/api/configurations/build/{created['build_id']}").status_code == 404


def test_delete_missing_returns_404(client, auth_headers):
    assert client.delete("/api/configurations/9999", headers=auth_headers).status_code == 404
