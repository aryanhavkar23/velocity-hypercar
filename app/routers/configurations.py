from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models import User
from app.schemas.configuration import (
    ConfigurationCreate, ConfigurationOut, ConfigurationUpdate, GarageOut, MessageOut,
    PublicConfigurationOut,
)
from app.services import configuration_service as svc
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/api/configurations", tags=["Configurations"])
garage_router = APIRouter(prefix="/api/garage", tags=["Garage"])


@router.post("", response_model=ConfigurationOut, status_code=status.HTTP_201_CREATED,
             summary="Create (save) a configuration",
             description="Send the selected option IDs. The server validates them and calculates price, "
                         "performance and a unique Build ID. Client-supplied prices/stats are ignored.")
def create_configuration(data: ConfigurationCreate, db: Session = Depends(get_db),
                         user: User = Depends(get_current_user)):
    config = svc.create_configuration(db, user, data.model_dump())
    return svc.build_configuration_response(config)


@router.get("", response_model=list[ConfigurationOut], summary="List my configurations",
            description="Returns every configuration owned by the logged-in user, newest first.")
def list_configurations(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return [svc.build_configuration_response(c) for c in svc.list_user_configurations(db, user)]


# Declared before /{configuration_id} so "build" is never treated as an id.
@router.get("/build/{build_id}", response_model=PublicConfigurationOut,
            summary="Get a shared build by Build ID (public)",
            description="No authentication required. Returns the full build without any private user data.")
def get_shared_build(build_id: str, db: Session = Depends(get_db)):
    return svc.build_public_response(svc.get_configuration_by_build_id(db, build_id))


@router.get("/{configuration_id}", response_model=ConfigurationOut, summary="Get one of my configurations",
            description="403 if the configuration belongs to another user, 404 if it does not exist.")
def get_configuration(configuration_id: int, db: Session = Depends(get_db),
                      user: User = Depends(get_current_user)):
    return svc.build_configuration_response(svc.get_owned_configuration(db, user, configuration_id))


@router.put("/{configuration_id}", response_model=ConfigurationOut, summary="Update a configuration",
            description="Send any option IDs/name to change. Price and performance are recalculated by the server.")
def update_configuration(configuration_id: int, data: ConfigurationUpdate, db: Session = Depends(get_db),
                         user: User = Depends(get_current_user)):
    config = svc.update_configuration(db, user, configuration_id, data.model_dump(exclude_unset=True))
    return svc.build_configuration_response(config)


@router.delete("/{configuration_id}", response_model=MessageOut, summary="Delete a configuration",
               description="Only the owner can delete. 403 for other users, 404 if it does not exist.")
def delete_configuration(configuration_id: int, db: Session = Depends(get_db),
                         user: User = Depends(get_current_user)):
    svc.delete_configuration(db, user, configuration_id)
    return {"message": "Configuration deleted successfully"}


@garage_router.get("", response_model=GarageOut, summary="My garage",
                   description="Summary list of the logged-in user's saved builds.")
def get_garage(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return svc.build_garage_response(svc.list_user_configurations(db, user))
