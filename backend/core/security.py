# JWT token management and user authentication

from datetime import datetime, timedelta, timezone
import jwt
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from starlette.status import HTTP_401_UNAUTHORIZED
from bson import ObjectId
from backend.core.config import settings
from backend.database.mongodb import get_db

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def create_access_token(subject: str) -> str:
    """Create JWT access token"""
    # Set expiration time (1 hour)
    expire = datetime.now(timezone.utc) + timedelta(hours=1)
    
    # Create token payload
    payload = {
        "sub": subject,
        "exp": expire
    }
    
    # Encode JWT token
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme), db=Depends(get_db)):
    """Validate JWT token and return user"""
    # Credentials exception for auth failures
    credentials_exception = HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Decode JWT token
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        
        # Extract user ID
        user_id: str = payload.get("sub")
        
        # Validate user ID
        if not user_id or not ObjectId.is_valid(user_id):
            raise credentials_exception
            
    except jwt.InvalidTokenError:
        raise credentials_exception

    # Find user in database
    user = await db["users"].find_one({"_id": ObjectId(user_id)})
    
    if not user:
        raise credentials_exception

    # Return user information
    return {
        "id": str(user["_id"]),
        "email": user["email"],
        "created_at": user["created_at"]
    }
