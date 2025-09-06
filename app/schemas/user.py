from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str
    is_active: bool = True
    email: str
    password: str


class UserSchema(BaseModel):
    id: int
    name: str
    is_active: bool
    email: str


class UserResponse(BaseModel):
    id: int
    name: str
