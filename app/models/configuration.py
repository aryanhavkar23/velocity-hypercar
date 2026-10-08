from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _fk(table: str):
    return mapped_column(ForeignKey(f"{table}.id"), nullable=False)


class Configuration(Base):
    __tablename__ = "configurations"

    id: Mapped[int] = mapped_column(primary_key=True)
    build_id: Mapped[str] = mapped_column(String(16), unique=True, index=True, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True, nullable=False)
    car_id: Mapped[int] = _fk("cars")

    paint_id: Mapped[int] = _fk("paints")
    wheel_id: Mapped[int] = _fk("wheels")
    caliper_id: Mapped[int] = _fk("calipers")

    interior_material_id: Mapped[int] = _fk("interior_materials")
    interior_color_id: Mapped[int] = _fk("interior_colors")
    seat_type_id: Mapped[int] = _fk("seat_types")

    engine_id: Mapped[int] = _fk("engines")
    performance_package_id: Mapped[int] = _fk("performance_packages")
    aero_package_id: Mapped[int] = _fk("aero_packages")

    calculated_price: Mapped[int] = mapped_column(Integer, nullable=False)
    calculated_horsepower: Mapped[int] = mapped_column(Integer, nullable=False)
    calculated_top_speed: Mapped[int] = mapped_column(Integer, nullable=False)
    calculated_acceleration: Mapped[float] = mapped_column(Float, nullable=False)
    calculated_handling: Mapped[int] = mapped_column(Integer, nullable=False)
    calculated_braking: Mapped[int] = mapped_column(Integer, nullable=False)

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=_now, nullable=False)

    user = relationship("User", back_populates="configurations")
    car = relationship("Car")
    paint = relationship("Paint")
    wheel = relationship("Wheel")
    caliper = relationship("Caliper")
    interior_material = relationship("InteriorMaterial")
    interior_color = relationship("InteriorColor")
    seat_type = relationship("SeatType")
    engine = relationship("Engine")
    performance_package = relationship("PerformancePackage")
    aero_package = relationship("AeroPackage")
