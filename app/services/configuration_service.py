"""Configuration business logic: validation, calculation, persistence, response building."""
from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models import (
    AeroPackage, Caliper, Car, Configuration, Engine, InteriorColor, InteriorMaterial,
    Paint, PerformancePackage, SeatType, User, Wheel,
)
from app.services.performance_service import calculate_performance
from app.services.pricing_service import calculate_configuration_price
from app.utils.build_id import generate_build_id, is_valid_build_id

# request field -> (model, attribute name used by the calculators)
SELECTION_FIELDS = {
    "car_id": (Car, "car"),
    "paint_id": (Paint, "paint"),
    "wheel_id": (Wheel, "wheel"),
    "caliper_id": (Caliper, "caliper"),
    "interior_material_id": (InteriorMaterial, "interior_material"),
    "interior_color_id": (InteriorColor, "interior_color"),
    "seat_type_id": (SeatType, "seat_type"),
    "engine_id": (Engine, "engine"),
    "performance_package_id": (PerformancePackage, "performance_package"),
    "aero_package_id": (AeroPackage, "aero_package"),
}


def _load_selection(db: Session, ids: dict[str, int]) -> dict:
    """Load every selected row; reject missing, inactive, or incompatible ones."""
    selection = {}
    car_id = ids.get("car_id")
    for field, (model, attr) in SELECTION_FIELDS.items():
        row = db.get(model, ids[field])
        if row is None:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, f"Invalid {field}: {ids[field]} does not exist")
        if not row.is_active:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, f"Invalid {field}: {ids[field]} is not available")
        if field != "car_id" and hasattr(row, "car_id") and row.car_id is not None:
            if car_id is not None and row.car_id != car_id:
                raise HTTPException(
                    status.HTTP_400_BAD_REQUEST,
                    f"Option '{row.name}' ({field}) is not compatible with car {car_id}",
                )
        selection[attr] = row
    return selection


def _apply_calculations(config: Configuration, selection: dict) -> None:
    pricing = calculate_configuration_price(**selection)
    stats = calculate_performance(
        selection["car"], selection["engine"], selection["performance_package"], selection["aero_package"]
    )
    config.calculated_price = pricing["final_price"]
    config.calculated_horsepower = stats["horsepower"]
    config.calculated_top_speed = stats["top_speed"]
    config.calculated_acceleration = stats["acceleration"]
    config.calculated_handling = stats["handling"]
    config.calculated_braking = stats["braking"]


def create_configuration(db: Session, user: User, data: dict) -> Configuration:
    ids = {field: data[field] for field in SELECTION_FIELDS}
    selection = _load_selection(db, ids)

    for _ in range(10):
        build_id = generate_build_id()
        if db.scalar(select(Configuration.id).where(Configuration.build_id == build_id)) is None:
            break
    else:
        raise HTTPException(status.HTTP_409_CONFLICT, "Could not allocate a unique build ID")

    config = Configuration(user_id=user.id, build_id=build_id, name=data["name"], **ids)
    _apply_calculations(config, selection)
    db.add(config)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status.HTTP_409_CONFLICT, "Build ID conflict, please retry")
    db.refresh(config)
    return config


def list_user_configurations(db: Session, user: User) -> list[Configuration]:
    stmt = (
        select(Configuration)
        .where(Configuration.user_id == user.id)
        .order_by(Configuration.updated_at.desc(), Configuration.id.desc())
    )
    return list(db.scalars(stmt).all())


def get_owned_configuration(db: Session, user: User, configuration_id: int) -> Configuration:
    config = db.get(Configuration, configuration_id)
    if config is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Configuration not found")
    if config.user_id != user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Configuration does not belong to this user")
    return config


def update_configuration(db: Session, user: User, configuration_id: int, changes: dict) -> Configuration:
    config = get_owned_configuration(db, user, configuration_id)
    changes = {k: v for k, v in changes.items() if v is not None}

    ids = {field: changes.get(field, getattr(config, field)) for field in SELECTION_FIELDS}
    selection = _load_selection(db, ids)

    for field, value in ids.items():
        setattr(config, field, value)
    if "name" in changes:
        config.name = changes["name"]
    _apply_calculations(config, selection)
    config.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(config)
    return config


def delete_configuration(db: Session, user: User, configuration_id: int) -> None:
    config = get_owned_configuration(db, user, configuration_id)
    db.delete(config)
    db.commit()


def get_configuration_by_build_id(db: Session, build_id: str) -> Configuration:
    build_id = build_id.strip().upper()
    if not is_valid_build_id(build_id):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Malformed build ID (expected format VX-XXXXX)")
    config = db.scalar(select(Configuration).where(Configuration.build_id == build_id))
    if config is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Build not found")
    return config


# ---------------------------------------------------------------- response builders

def _sections(c: Configuration) -> dict:
    return {
        "exterior": {
            "paint": {"id": c.paint.id, "name": c.paint.name, "hex_code": c.paint.hex_code},
            "wheels": {"id": c.wheel.id, "name": c.wheel.name},
            "caliper": {"id": c.caliper.id, "name": c.caliper.name},
        },
        "interior": {
            "material": {"id": c.interior_material.id, "name": c.interior_material.name},
            "color": {"id": c.interior_color.id, "name": c.interior_color.name},
            "seat": {"id": c.seat_type.id, "name": c.seat_type.name},
        },
        "performance": {
            "engine": {"id": c.engine.id, "name": c.engine.name},
            "package": {"id": c.performance_package.id, "name": c.performance_package.name},
            "aero": {"id": c.aero_package.id, "name": c.aero_package.name},
            "stats": {
                "horsepower": c.calculated_horsepower,
                "top_speed": c.calculated_top_speed,
                "acceleration": c.calculated_acceleration,
                "handling": c.calculated_handling,
                "braking": c.calculated_braking,
            },
        },
        "pricing": {
            "base_price": c.car.base_price,
            "options_total": c.calculated_price - c.car.base_price,
            "final_price": c.calculated_price,
        },
        "created_at": c.created_at,
        "updated_at": c.updated_at,
    }


def build_configuration_response(c: Configuration) -> dict:
    return {
        "id": c.id,
        "build_id": c.build_id,
        "name": c.name,
        "car": {"id": c.car.id, "name": c.car.name},
        **_sections(c),
    }


def build_public_response(c: Configuration) -> dict:
    return {"build_id": c.build_id, "name": c.name, "car": c.car, **_sections(c)}


def build_garage_response(configs: list[Configuration]) -> dict:
    return {
        "builds": [
            {
                "id": c.id,
                "build_id": c.build_id,
                "name": c.name,
                "car": c.car.name,
                "price": c.calculated_price,
                "created_at": c.created_at,
                "updated_at": c.updated_at,
            }
            for c in configs
        ]
    }
