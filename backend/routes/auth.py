# Authentication routes for user signup, login, and user info

from fastapi import APIRouter, Depends, HTTPException, status
from datetime import datetime, timezone
from bson import ObjectId
from pymongo.errors import DuplicateKeyError

from backend.schemas.user import UserCreate, UserLogin, UserPublic, Token
from backend.utils.hash import hash_password, verify_password
from backend.database.mongodb import get_db
from backend.core.security import create_access_token, get_current_user

# Router with /auth prefix
router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/signup", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
async def signup(payload: UserCreate, db=Depends(get_db)):
    """Register a new user"""
    # Check if database is available
    if db is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database service unavailable"
        )
    
    # Normalize email
    email = payload.email.lower().strip()
    
    # Check if user exists
    existing_user = await db["users"].find_one({"email": email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )
    
    # Create user with hashed password
    user_data = {
        "email": email,
        "password_hash": hash_password(payload.password),
        "created_at": datetime.now(timezone.utc),
        "is_active": True
    }
    
    try:
        # Insert user
        result = await db["users"].insert_one(user_data)
        user = await db["users"].find_one({"_id": result.inserted_id})
        
        # Return user data
        return {
            "id": str(user["_id"]),
            "email": user["email"],
            "created_at": user["created_at"]
        }
    except DuplicateKeyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )

@router.post("/login", response_model=Token)
async def login(payload: UserLogin, db=Depends(get_db)):
    """Login user and return JWT token"""
    # Check if database is available
    if db is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database service unavailable"
        )
    
    # Normalize email
    email = payload.email.lower().strip()
    
    # Find user by email
    user = await db["users"].find_one({"email": email})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Check if account is active
    if not user.get("is_active", True):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Account is disabled"
        )
    
    # Verify password
    if not verify_password(payload.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Generate JWT token
    access_token = create_access_token(subject=str(user["_id"]))
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.get("/me", response_model=UserPublic)
async def get_current_user_info(current_user=Depends(get_current_user)):
    """Get current user information"""
    return current_user