from pydantic import BaseModel, Field, field_validator
from typing import Optional
import re

EMAIL_REGEX = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

class UserRegisterRequest(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=100)
    company_name: str = Field(..., min_length=2, max_length=100)
    email: str = Field(..., min_length=5, max_length=150)
    password: str = Field(..., min_length=6)
    role: Optional[str] = "Port Operator"

    @field_validator('email')
    @classmethod
    def validate_email_format(cls, v: str) -> str:
        clean = v.strip().lower()
        if not re.match(EMAIL_REGEX, clean):
            raise ValueError('Invalid email format')
        return clean

class UserLoginRequest(BaseModel):
    email: str = Field(..., min_length=3)
    password: str
    remember_me: Optional[bool] = False

    @field_validator('email')
    @classmethod
    def clean_email(cls, v: str) -> str:
        return v.strip().lower()

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict

class UserResponse(BaseModel):
    id: int
    full_name: str
    company_name: str
    email: str
    role: str

    class Config:
        from_attributes = True
