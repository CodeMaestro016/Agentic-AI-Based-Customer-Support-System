# Application configuration using Pydantic Settings

from pydantic_settings import BaseSettings, SettingsConfigDict
import os
from pathlib import Path

class Settings(BaseSettings):
    """Application settings from environment variables.

    Provide sensible development defaults so the application can start
    without requiring every environment variable during local development.
    In production, override these using a `.env` file or real environment
    variables.
    """

    # MongoDB configuration (default to local MongoDB for development)
    MONGO_URI: str = "mongodb://localhost:27017"
    MONGO_DB_NAME: str = "customer_support_db"

    # JWT authentication configuration
    JWT_SECRET: str = "dev-secret-change-me"
    JWT_ALGORITHM: str = "HS256"

    # OpenAI API configuration (empty by default; set in env for production)
    OPENAI_API_KEY: str = ""

    # Configuration for settings loading
    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent.parent.parent / ".env",  # Look for .env in project root
        env_file_encoding="utf-8",
        extra="ignore",  # Ignore extra fields instead of raising validation error
        case_sensitive=False,  # Allow case-insensitive environment variable names
    )

# Global settings instance
settings = Settings()