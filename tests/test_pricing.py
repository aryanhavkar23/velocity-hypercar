from types import SimpleNamespace as NS

from app.services.pricing_service import calculate_configuration_price


def _parts(**overrides):
    parts = dict(
        car=NS(base_price=24_000_000),
        paint=NS(price_modifier=0), wheel=NS(price_modifier=0), caliper=NS(price_modifier=0),
        interior_material=NS(price_modifier=0), interior_color=NS(price_modifier=0),
        seat_type=NS(price_modifier=0), engine=NS(price_modifier=0),
        performance_package=NS(price_modifier=0), aero_package=NS(price_modifier=0),
    )
    for key, value in overrides.items():
        parts[key] = NS(price_modifier=value) if key != "car" else NS(base_price=value)
    return parts


def test_base_car_price_only():
    result = calculate_configuration_price(**_parts())
    assert result == {"base_price": 24_000_000, "options_total": 0, "final_price": 24_000_000}


def test_single_option_modifier():
    result = calculate_configuration_price(**_parts(paint=200_000))
    assert result["options_total"] == 200_000 and result["final_price"] == 24_200_000


def test_every_modifier_is_counted():
    mods = dict(paint=1, wheel=10, caliper=100, interior_material=1_000, interior_color=10_000,
                seat_type=100_000, engine=1_000_000, performance_package=10_000_000,
                aero_package=100_000_000)
    result = calculate_configuration_price(**_parts(**mods))
    assert result["options_total"] == 111_111_111
    assert result["final_price"] == 24_000_000 + 111_111_111


def test_final_price_is_base_plus_options():
    result = calculate_configuration_price(**_parts(car=10, engine=5, aero_package=7))
    assert result["final_price"] == result["base_price"] + result["options_total"] == 22


def test_prices_are_integers():
    result = calculate_configuration_price(**_parts(engine=2_000_000))
    assert all(isinstance(v, int) for v in result.values())


def test_seeded_scenario_price_via_api(client, auth_headers, payload):
    r = client.post("/api/configurations", json=payload, headers=auth_headers)
    # Carbon wheels 450k + Red caliper 25k + Alcantara 350k + Racing 250k
    # + Weissach Power 1.8M + Weissach Package 3.5M + Active DRS Aero 900k = 7,275,000
    assert r.json()["pricing"] == {
        "base_price": 35_000_000, "options_total": 7_275_000, "final_price": 42_275_000,
    }
