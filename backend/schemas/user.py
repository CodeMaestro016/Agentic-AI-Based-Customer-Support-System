# Pydantic models for user data validation

from pydantic import BaseModel
from datetime import datetime

# Use plain str for emails here to avoid importing the optional
# `email-validator` dependency at process startup. This is a small
# pragmatic change to unblock the dev server; if you want stricter
# email validation, install `email-validator` or switch back to
# `EmailStr` once the environment is consistent.
class UserCreate(BaseModel):
    """User registration request"""
    email: str
    password: str


class UserLogin(BaseModel):
    """User login request"""
    email: str
    password: str


class UserPublic(BaseModel):
    """User data for API responses"""
    id: str
    email: str
    created_at: datetime


class Token(BaseModel):
    """JWT token response"""
    access_token: str
    token_type: str = "bearer"
