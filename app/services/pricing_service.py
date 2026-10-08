"""Price calculation. All amounts are integer INR; no floating point."""


def calculate_configuration_price(
    car, paint, wheel, caliper, interior_material, interior_color,
    seat_type, engine, performance_package, aero_package,
) -> dict[str, int]:
    options_total = (
        paint.price_modifier
        + wheel.price_modifier
        + caliper.price_modifier
        + interior_material.price_modifier
        + interior_color.price_modifier
        + seat_type.price_modifier
        + engine.price_modifier
        + performance_package.price_modifier
        + aero_package.price_modifier
    )
    base_price = car.base_price
    return {
        "base_price": base_price,
        "options_total": options_total,
        "final_price": base_price + options_total,
    }
