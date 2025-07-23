from pydantic import BaseModel, EmailStr
from typing import Optional
from .models import Role

# User Schemas
class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str
    role: Role = Role.USER

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    role: Optional[Role] = None

class User(UserBase):
    id: int
    role: Role

    class Config:
        from_attributes = True

# Token Schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None