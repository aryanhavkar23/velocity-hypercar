from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models import (
    AeroPackage, Caliper, Engine, InteriorColor, InteriorMaterial, Paint,
    PerformancePackage, SeatType, Wheel,
)
from app.schemas import options as s

router = APIRouter(prefix="/api/options", tags=["Options"])

# (url path, response key, model, schema, human label)
_OPTIONS = [
    ("paints", "paints", Paint, s.PaintOut, "paint colours"),
    ("wheels", "wheels", Wheel, s.WheelOut, "wheel designs"),
    ("calipers", "calipers", Caliper, s.CaliperOut, "brake caliper colours"),
    ("interior-materials", "interior_materials", InteriorMaterial, s.InteriorMaterialOut, "interior materials"),
    ("interior-colors", "interior_colors", InteriorColor, s.InteriorColorOut, "interior colours"),
    ("seat-types", "seat_types", SeatType, s.SeatTypeOut, "seat types"),
    ("engines", "engines", Engine, s.EngineOut, "engines"),
    ("performance-packages", "performance_packages", PerformancePackage, s.PerformancePackageOut, "performance packages"),
    ("aero-packages", "aero_packages", AeroPackage, s.AeroPackageOut, "aero packages"),
]


def _active(db: Session, model, car_id: int | None = None):
    stmt = select(model).where(model.is_active.is_(True))
    if car_id is not None:
        stmt = stmt.where((model.car_id.is_(None)) | (model.car_id == car_id))
    return db.scalars(stmt.order_by(model.id)).all()


@router.get("", response_model=s.OptionsOut, summary="All customization options",
            description="Returns active options grouped by category. Inactive options are excluded. Pass car_id to filter compatible options.")
def all_options(car_id: int | None = None, db: Session = Depends(get_db)):
    return {key: _active(db, model, car_id=car_id) for _, key, model, _, _ in _OPTIONS}


def _register(path: str, model, schema, label: str) -> None:
    def endpoint(car_id: int | None = None, db: Session = Depends(get_db)):
        return _active(db, model, car_id=car_id)

    endpoint.__name__ = f"list_{path.replace('-', '_')}"
    router.add_api_route(
        f"/{path}", endpoint, methods=["GET"], response_model=list[schema],
        summary=f"List {label}", description=f"Returns active {label}. Pass car_id to filter compatible options.",
    )


for _path, _key, _model, _schema, _label in _OPTIONS:
    _register(_path, _model, _schema, _label)
