from pydantic import BaseModel

from app.schemas.user import UserSchema


class LoginRequest(BaseModel):
    email: str
    password: str


class AuthReponse(BaseModel):
    user: UserSchema
    token: str
