from pydantic import BaseModel, EmailStr, Field
from datetime import datetime, date
from typing import Optional

from sqlalchemy import DateTime

class AccountResponse(BaseModel):
    id: int
    account_number: str
    balance: float|None = None

    class Config:
        orm_mode = True  # This allows pydantic to work with ORM models like SQLAlchemy
        from_attributes = True




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
    account : AccountResponse

    class Config:
        orm_mode = True
        from_attributes = True


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
    class_id: int|None = None
    avatar: str | None = None

    class Config:
        orm_mode = True
        from_attributes = True


class ChildCreate(BaseModel):
    first_name: str
    last_name: str
    birth_date: date
    avatar: str | None = None

    class Config:
        orm_mode = True
        from_attributes = True


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
        from_attributes = True


class ClassCreate(BaseModel):
    name: str

    class Config:
        orm_mode = True
        from_attributes = True


class ClassModify(BaseModel):
    name : str
    class Config:
        orm_mode = True
        from_attributes = True


class AddChildToClass(BaseModel):
    child_id: int
    class_id: int
    class Config:
        orm_mode = True
        from_attributes = True


# Request schema to create a collection
class CollectionCreate(BaseModel):
    title: str
    goal : float
    description: str
    start_date: datetime
    end_date: datetime
    class_id: int

    class Config:
        orm_mode = True  # This allows us to work with ORM models directly
        from_attributes = True


class CollectionModify(BaseModel):
    goal : float|None = None
    title : str|None = None
    description :str|None = None
    end_date : date|None = None


# Response schema to return created collection
class CollectionResponse(BaseModel):
    id: int
    goal : float
    title: str
    description: str
    start_date: datetime
    end_date: datetime
    class_id: int
    creator_id: int
    account : AccountResponse

    class Config:
        orm_mode = True
        from_attributes = True



class FinancialTransactionCreate(BaseModel):
    account_number: str = Field(..., description="Destination account number")
    amount: float = Field(..., gt=0, description="Transfer amount (must be greater than 0)")
    description: str = Field(None, description="Optional transfer description")
    child_id : int | None = None


class FinancialTransactionResponse(BaseModel):
    source: CollectionResponse|UserResponse
    destination: CollectionResponse|UserResponse
    amount: float
    timestamp : datetime
    description: str | None
    child : ChildResponse| None = None

class CreateInviteRequest(BaseModel):
    class_id : int
    expiration_minutes : int = 6 * 60

class ProcessInviteRequest(BaseModel):
    child_id: int