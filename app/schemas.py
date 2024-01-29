from datetime import datetime
from typing import List
import uuid
from pydantic import BaseModel, EmailStr, constr
from .models import AdTypes, UserRole


class UserBaseSchema(BaseModel):
    name: str
    email: EmailStr
    photo: str
    phone_number: str

    class Config:
        orm_mode = True


class CreateUserSchema(UserBaseSchema):
    password: constr(min_length=8)
    passwordConfirm: str
    role: UserRole = UserRole.user
    is_superuser: bool = False
    verified: bool = False


class LoginUserSchema(BaseModel):
    email: EmailStr
    password: constr(min_length=8)

    class Config:
        orm_mode = True


class UserResponse(UserBaseSchema):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class FilteredUserResponse(UserBaseSchema):
    id: uuid.UUID


class AdBaseSchema(BaseModel):
    title: str
    description: str
    type: AdTypes
    user_id: uuid.UUID | None = None

    class Config:
        orm_mode = True


class CreateAdSchema(AdBaseSchema):
    pass


class AdResponse(AdBaseSchema):
    id: int
    user: FilteredUserResponse
    created_at: datetime
    updated_at: datetime


class UpdateAdSchema(BaseModel):
    title: str
    description: str
    type: AdTypes
    user_id: uuid.UUID | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        orm_mode = True


class ListAdResponse(BaseModel):
    status: str
    results: int
    ads: List[AdResponse]

    
