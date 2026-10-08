from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models import Car
from app.schemas.car import CarOut

router = APIRouter(prefix="/api/cars", tags=["Cars"])


@router.get("", response_model=list[CarOut], summary="List available cars",
            description="Returns all active hypercars, ordered by id.")
def list_cars(db: Session = Depends(get_db)):
    return db.scalars(select(Car).where(Car.is_active.is_(True)).order_by(Car.id)).all()


@router.get("/{car_id}", response_model=CarOut, summary="Get one car",
            description="Returns a single active car, or 404 if it does not exist or is inactive.")
def get_car(car_id: int, db: Session = Depends(get_db)):
    car = db.get(Car, car_id)
    if car is None or not car.is_active:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Car not found")
    return car
