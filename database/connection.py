"""
Database connection management
"""

import logging
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from config import config

logger = logging.getLogger(__name__)

# Global database instance
db: AsyncIOMotorDatabase = None


async def init_db() -> AsyncIOMotorDatabase:
    """Initialize MongoDB connection"""
    global db
    
    try:
        client = AsyncIOMotorClient(config.DATABASE_URL)
        db = client[config.MONGODB_DATABASE]
        
        # Test connection
        await db.command('ping')
        logger.info(f"Connected to MongoDB: {config.MONGODB_DATABASE}")
        
        return db
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        raise


def get_db() -> AsyncIOMotorDatabase:
    """Get database instance"""
    if db is None:
        raise RuntimeError("Database not initialized. Call init_db() first.")
    return db
