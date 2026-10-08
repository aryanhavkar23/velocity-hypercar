from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.car import CarOut

PositiveId = Field(gt=0)


class ConfigurationCreate(BaseModel):
    """Selected option IDs only. Any price/stat fields sent by the client are ignored."""
    model_config = ConfigDict(extra="ignore", str_strip_whitespace=True)

    car_id: int = PositiveId
    paint_id: int = PositiveId
    wheel_id: int = PositiveId
    caliper_id: int = PositiveId
    interior_material_id: int = PositiveId
    interior_color_id: int = PositiveId
    seat_type_id: int = PositiveId
    engine_id: int = PositiveId
    performance_package_id: int = PositiveId
    aero_package_id: int = PositiveId
    name: str = Field(default="Untitled Build", min_length=1, max_length=100)


class ConfigurationUpdate(BaseModel):
    """Every field optional; omitted fields keep their current value."""
    model_config = ConfigDict(extra="ignore", str_strip_whitespace=True)

    car_id: int | None = Field(default=None, gt=0)
    paint_id: int | None = Field(default=None, gt=0)
    wheel_id: int | None = Field(default=None, gt=0)
    caliper_id: int | None = Field(default=None, gt=0)
    interior_material_id: int | None = Field(default=None, gt=0)
    interior_color_id: int | None = Field(default=None, gt=0)
    seat_type_id: int | None = Field(default=None, gt=0)
    engine_id: int | None = Field(default=None, gt=0)
    performance_package_id: int | None = Field(default=None, gt=0)
    aero_package_id: int | None = Field(default=None, gt=0)
    name: str | None = Field(default=None, min_length=1, max_length=100)


class Ref(BaseModel):
    id: int
    name: str


class ColorRef(Ref):
    hex_code: str


class ExteriorOut(BaseModel):
    paint: ColorRef
    wheels: Ref
    caliper: Ref


class InteriorOut(BaseModel):
    material: Ref
    color: Ref
    seat: Ref


class StatsOut(BaseModel):
    horsepower: int
    top_speed: int
    acceleration: float
    handling: int
    braking: int


class PerformanceOut(BaseModel):
    engine: Ref
    package: Ref
    aero: Ref
    stats: StatsOut


class PricingOut(BaseModel):
    base_price: int
    options_total: int
    final_price: int


class ConfigurationOut(BaseModel):
    id: int
    build_id: str
    name: str
    car: Ref
    exterior: ExteriorOut
    interior: InteriorOut
    performance: PerformanceOut
    pricing: PricingOut
    created_at: datetime
    updated_at: datetime


class PublicConfigurationOut(BaseModel):
    """Shared-build view: no user id/email and no internal row id."""
    build_id: str
    name: str
    car: CarOut
    exterior: ExteriorOut
    interior: InteriorOut
    performance: PerformanceOut
    pricing: PricingOut
    created_at: datetime
    updated_at: datetime


class GarageBuild(BaseModel):
    id: int
    build_id: str
    name: str
    car: str
    price: int
    created_at: datetime
    updated_at: datetime


class GarageOut(BaseModel):
    builds: list[GarageBuild]


class MessageOut(BaseModel):
    message: str
