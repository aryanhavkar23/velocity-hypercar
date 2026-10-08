from pydantic import BaseModel, Field

from app.schemas.user import UserPublic


class LoginRequest(BaseModel):
    email: str = Field(examples=["user@example.com"])
    password: str = Field(examples=["password123"])


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserPublic
