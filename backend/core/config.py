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
    
    # OpenAI API configuration
    OPENAI_API_KEY: str

    # Configuration for settings loading
    model_config = SettingsConfigDict(
        env_file="../.env",
        env_file_encoding="utf-8",
        extra="ignore",  # Ignore extra fields instead of raising validation error
        case_sensitive=False,  # Allow case-insensitive environment variable names
    )

# Global settings instance
settings = Settings()
