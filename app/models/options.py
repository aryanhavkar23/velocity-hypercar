from sqlalchemy import Boolean, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class _OptionMixin:
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    price_modifier: Mapped[int] = mapped_column(Integer, default=0, nullable=False)  # INR
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    car_id: Mapped[int | None] = mapped_column(ForeignKey("cars.id"), nullable=True, default=None)


class Paint(_OptionMixin, Base):
    __tablename__ = "paints"
    hex_code: Mapped[str] = mapped_column(String(7), nullable=False)
    category: Mapped[str] = mapped_column(String(50), default="solid", nullable=False)


class Wheel(_OptionMixin, Base):
    __tablename__ = "wheels"
    description: Mapped[str] = mapped_column(Text, default="", nullable=False)
    # Stored for future use; the spec only lets engine/package/aero affect stats.
    performance_modifier: Mapped[int] = mapped_column(Integer, default=0, nullable=False)


class Caliper(_OptionMixin, Base):
    __tablename__ = "calipers"
    hex_code: Mapped[str] = mapped_column(String(7), nullable=False)


class InteriorMaterial(_OptionMixin, Base):
    __tablename__ = "interior_materials"
    description: Mapped[str] = mapped_column(Text, default="", nullable=False)


class InteriorColor(_OptionMixin, Base):
    __tablename__ = "interior_colors"
    hex_code: Mapped[str] = mapped_column(String(7), nullable=False)


class SeatType(_OptionMixin, Base):
    __tablename__ = "seat_types"
    description: Mapped[str] = mapped_column(Text, default="", nullable=False)


class _StatModifierMixin(_OptionMixin):
    description: Mapped[str] = mapped_column(Text, default="", nullable=False)
    horsepower_modifier: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    top_speed_modifier: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    acceleration_modifier: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    handling_modifier: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    braking_modifier: Mapped[int] = mapped_column(Integer, default=0, nullable=False)


class Engine(_StatModifierMixin, Base):
    __tablename__ = "engines"


class PerformancePackage(_StatModifierMixin, Base):
    __tablename__ = "performance_packages"


class AeroPackage(_OptionMixin, Base):
    __tablename__ = "aero_packages"
    description: Mapped[str] = mapped_column(Text, default="", nullable=False)
    downforce: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    drag: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    handling_modifier: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    top_speed_modifier: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
