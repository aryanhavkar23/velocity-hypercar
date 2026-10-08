from pydantic import BaseModel, ConfigDict


class _ORM(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    car_id: int | None = None


class PaintOut(_ORM):
    id: int
    name: str
    hex_code: str
    category: str
    price_modifier: int


class WheelOut(_ORM):
    id: int
    name: str
    description: str
    price_modifier: int
    performance_modifier: int


class CaliperOut(_ORM):
    id: int
    name: str
    hex_code: str
    price_modifier: int


class InteriorMaterialOut(_ORM):
    id: int
    name: str
    description: str
    price_modifier: int


class InteriorColorOut(_ORM):
    id: int
    name: str
    hex_code: str
    price_modifier: int


class SeatTypeOut(_ORM):
    id: int
    name: str
    description: str
    price_modifier: int


class _StatOptionOut(_ORM):
    id: int
    name: str
    description: str
    price_modifier: int
    horsepower_modifier: int
    top_speed_modifier: int
    acceleration_modifier: float
    handling_modifier: int
    braking_modifier: int


class EngineOut(_StatOptionOut):
    pass


class PerformancePackageOut(_StatOptionOut):
    pass


class AeroPackageOut(_ORM):
    id: int
    name: str
    description: str
    price_modifier: int
    downforce: int
    drag: int
    handling_modifier: int
    top_speed_modifier: int


class OptionsOut(BaseModel):
    paints: list[PaintOut]
    wheels: list[WheelOut]
    calipers: list[CaliperOut]
    interior_materials: list[InteriorMaterialOut]
    interior_colors: list[InteriorColorOut]
    seat_types: list[SeatTypeOut]
    engines: list[EngineOut]
    performance_packages: list[PerformancePackageOut]
    aero_packages: list[AeroPackageOut]
