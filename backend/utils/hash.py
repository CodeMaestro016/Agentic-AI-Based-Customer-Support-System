# Password hashing utilities using bcrypt and data hashing using SHA256

from passlib.context import CryptContext
import hashlib

# Password context with bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash plaintext password using bcrypt"""
    return pwd_context.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    """Verify plaintext password against hash"""
    return pwd_context.verify(password, hashed)

def hash_chat_details(data: str) -> str:
    """Hash chat details JSON string using SHA256 for integrity"""
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

def verify_chat_hash(plain_data: str, stored_hash: str) -> bool:
    """Verify if the plain data matches the stored hash"""
    return hash_chat_details(plain_data) == stored_hash
