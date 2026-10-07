from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.security import create_access_token
from app.db.database import get_db
from app.models import User
from app.schemas.auth import LoginRequest, TokenResponse
from app.schemas.user import UserCreate, UserPublic
from app.services import auth_service

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/register", response_model=UserPublic, status_code=status.HTTP_201_CREATED,
             summary="Register a new user",
             description="Creates an account. Email and username must be unique. Password: 8-72 characters.")
def register(data: UserCreate, db: Session = Depends(get_db)):
    return auth_service.register_user(db, data)


@router.post("/login", response_model=TokenResponse, summary="Log in and receive a JWT",
             description="Returns a bearer token. Send it as `Authorization: Bearer <token>`.")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = auth_service.authenticate_user(db, data.email, data.password)
    return {"access_token": create_access_token(str(user.id)), "token_type": "bearer", "user": user}


@router.get("/me", response_model=UserPublic, summary="Get the current user",
            description="Returns the profile of the user identified by the bearer token.")
def me(user: User = Depends(auth_service.get_current_user)):
    return user
