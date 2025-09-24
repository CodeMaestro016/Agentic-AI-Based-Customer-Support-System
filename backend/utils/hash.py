# Password hashing utilities using bcrypt

from passlib.context import CryptContext

# Password context with bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash plaintext password using bcrypt"""
    return pwd_context.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    """Verify plaintext password against hash"""
    return pwd_context.verify(password, hashed)
