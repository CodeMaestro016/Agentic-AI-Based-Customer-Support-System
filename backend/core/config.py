# Application configuration using Pydantic Settings

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Application settings from environment variables"""
    
    # MongoDB configuration
    MONGO_URI: str
    MONGO_DB_NAME: str
    
    # JWT authentication configuration
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"

    # Configuration for settings loading
    model_config = SettingsConfigDict(
        env_file="../.env",
        env_file_encoding="utf-8",
    )

# Global settings instance
settings = Settings()
