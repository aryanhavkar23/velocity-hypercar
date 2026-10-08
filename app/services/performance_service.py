"""Performance calculation: car base stats + engine + performance package + aero."""


def _clamp(value: int, low: int, high: int) -> int:
    return max(low, min(high, value))


def calculate_performance(car, engine, performance_package, aero_package) -> dict:
    horsepower = car.horsepower + engine.horsepower_modifier + performance_package.horsepower_modifier
    top_speed = (
        car.top_speed
        + engine.top_speed_modifier
        + performance_package.top_speed_modifier
        + aero_package.top_speed_modifier
    )
    acceleration = (
        car.acceleration + engine.acceleration_modifier + performance_package.acceleration_modifier
    )
    handling = (
        car.handling
        + engine.handling_modifier
        + performance_package.handling_modifier
        + aero_package.handling_modifier
    )
    braking = car.braking + engine.braking_modifier + performance_package.braking_modifier

    return {
        "horsepower": max(0, int(horsepower)),
        "top_speed": max(0, int(top_speed)),
        # Lower is better; never faster than 1.0s. Rounded to avoid float noise.
        "acceleration": max(1.0, round(acceleration, 2)),
        "handling": _clamp(int(handling), 0, 100),
        "braking": _clamp(int(braking), 0, 100),
    }
