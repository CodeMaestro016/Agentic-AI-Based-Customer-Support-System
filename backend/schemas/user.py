# Pydantic models for user data validation

from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    """User registration request"""
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    """User login request"""
    email: EmailStr
    password: str

class UserPublic(BaseModel):
    """User data for API responses"""
    id: str
    email: EmailStr
    created_at: datetime
    is_admin: bool = False

class Token(BaseModel):
    """JWT token response"""
    access_token: str
    token_type: str = "bearer"

class AdminLogin(BaseModel):
    """Admin login request"""
    email: EmailStr
    password: str

class AdminPublic(BaseModel):
    """Admin data for API responses"""
    id: str
    email: EmailStr
    created_at: datetime
    is_admin: bool = True
