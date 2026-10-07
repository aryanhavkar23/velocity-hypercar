from types import SimpleNamespace as NS

from app.services.performance_service import calculate_performance

CAR = NS(horsepower=950, top_speed=380, acceleration=2.1, handling=82, braking=86)
ZERO_STAT = dict(horsepower_modifier=0, top_speed_modifier=0, acceleration_modifier=0.0,
                 handling_modifier=0, braking_modifier=0)
NO_ENGINE = NS(**ZERO_STAT)
NO_PACKAGE = NS(**ZERO_STAT)
NO_AERO = NS(handling_modifier=0, top_speed_modifier=0)


def test_no_modifiers_returns_car_stats():
    assert calculate_performance(CAR, NO_ENGINE, NO_PACKAGE, NO_AERO) == {
        "horsepower": 950, "top_speed": 380, "acceleration": 2.1, "handling": 82, "braking": 86,
    }


def test_engine_modifies_horsepower():
    engine = NS(**{**ZERO_STAT, "horsepower_modifier": 150})
    assert calculate_performance(CAR, engine, NO_PACKAGE, NO_AERO)["horsepower"] == 1100


def test_package_modifies_stats():
    pkg = NS(horsepower_modifier=80, top_speed_modifier=5, acceleration_modifier=-0.1,
             handling_modifier=8, braking_modifier=8)
    result = calculate_performance(CAR, NO_ENGINE, pkg, NO_AERO)
    assert result == {"horsepower": 1030, "top_speed": 385, "acceleration": 2.0, "handling": 90, "braking": 94}


def test_aero_modifies_handling_and_top_speed():
    aero = NS(handling_modifier=10, top_speed_modifier=-8)
    result = calculate_performance(CAR, NO_ENGINE, NO_PACKAGE, aero)
    assert result["handling"] == 92 and result["top_speed"] == 372
    assert result["horsepower"] == 950 and result["braking"] == 86


def test_acceleration_floor_is_one_second():
    engine = NS(**{**ZERO_STAT, "acceleration_modifier": -5.0})
    assert calculate_performance(CAR, engine, NO_PACKAGE, NO_AERO)["acceleration"] == 1.0


def test_handling_and_braking_clamped_to_0_100():
    pkg = NS(**{**ZERO_STAT, "handling_modifier": 50, "braking_modifier": 50})
    high = calculate_performance(CAR, NO_ENGINE, pkg, NO_AERO)
    assert high["handling"] == 100 and high["braking"] == 100
    pkg = NS(**{**ZERO_STAT, "handling_modifier": -500, "braking_modifier": -500})
    low = calculate_performance(CAR, NO_ENGINE, pkg, NO_AERO)
    assert low["handling"] == 0 and low["braking"] == 0


def test_acceleration_has_no_float_noise():
    engine = NS(**{**ZERO_STAT, "acceleration_modifier": -0.1})
    pkg = NS(**{**ZERO_STAT, "acceleration_modifier": -0.1})
    assert calculate_performance(CAR, engine, pkg, NO_AERO)["acceleration"] == 1.9


def test_seeded_scenario_stats_via_api(client, auth_headers, payload):
    stats = client.post("/api/configurations", json=payload, headers=auth_headers).json()["performance"]["stats"]
    # Porsche 911 GT3 RS (525hp, 296km/h, 3.2s, 98, 97)
    # + Weissach Power (+20hp, +4, -0.1, +1, 0)
    # + Weissach Package (+50hp, +5, -0.1, +8, +8)
    # + Active DRS Aero (+8 hnd, -3 top)
    assert stats == {"horsepower": 595, "top_speed": 302, "acceleration": 3.0, "handling": 100, "braking": 100}
