from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str
    is_active: bool = True
    
class UserSchema(BaseModel):
    id: int
    name: str
    is_active: bool