from typing import Literal
from pydantic import BaseModel, EmailStr, Field


class UserRegister(BaseModel):
    """Public self-registration. Always creates a patient account — doctor
    and admin accounts are provisioned separately by an existing admin
    (see StaffCreate / POST /admin/users), never chosen by the registrant."""

    email: EmailStr
    password: str = Field(min_length=8)
    full_name: str


class StaffCreate(BaseModel):
    """Used by an existing admin to create a doctor or admin account."""

    email: EmailStr
    password: str = Field(min_length=8)
    full_name: str
    role: Literal["doctor", "admin"]


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"