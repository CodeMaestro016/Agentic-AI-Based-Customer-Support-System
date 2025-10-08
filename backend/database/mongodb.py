# MongoDB connection and management

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from fastapi import Depends
from backend.core.config import settings
import logging

# Setup logging
logger = logging.getLogger(__name__)

# Global database connection variables
_client: AsyncIOMotorClient | None = None
_db: AsyncIOMotorDatabase | None = None

async def connect_to_mongo():
    """Initialize MongoDB connection"""
    global _client, _db
    try:
        # Create async MongoDB client
        _client = AsyncIOMotorClient(settings.MONGO_URI)
        
        # Get database instance
        _db = _client[settings.MONGO_DB_NAME]
        
        # Test connection
        await _client.admin.command('ping')
        
        # Create unique index on email field
        await _db["users"].create_index("email", unique=True)
        
        print("✅ MongoDB connection successful")
        logger.info("MongoDB connected successfully")
        
    except Exception as e:
        print(f"❌ Failed to connect to MongoDB: {e}")
        logger.error(f"Failed to connect to MongoDB: {e}")
        # Don't raise the exception, allow the application to start without DB
        # This is for development purposes only
        print("⚠️  Application will start without database connection - some features may not work")
        _client = None
        _db = None

async def close_mongo_connection():
    """Close MongoDB connection"""
    global _client
    if _client:
        _client.close()
        print("🔌 MongoDB connection closed")
        logger.info("MongoDB connection closed")

async def get_db() -> AsyncIOMotorDatabase:
    """Get database instance for dependency injection"""
    global _db
    if _db is None:
        # Return None if no database connection
        return None
    return _db
