from pydantic import BaseModel, EmailStr
from datetime import datetime, date
from typing import Optional

from sqlalchemy import DateTime


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    created_at: datetime

    class Config:
        orm_mode = True


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class ChildResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    birth_date: date
    avatar: str | None = None

    class Config:
        orm_mode = True


class ChildCreate(BaseModel):
    first_name: str
    last_name: str
    birth_date: date
    avatar: str | None = None

    class Config:
        orm_mode = True


class ChildModify(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    birth_date: Optional[date] = None

    class Config:
        orm_mode = True


class ClassResponse(BaseModel):
    id: int
    name: str
    treasurer_id: int
    created_at: datetime

    class Config:
        orm_mode = True  # Allows Pydantic to work with SQLAlchemy models


class ClassCreate(BaseModel):
    name: str

    class Config:
        orm_mode = True


class ClassModify(BaseModel):
    name : str
