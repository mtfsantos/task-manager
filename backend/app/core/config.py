import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from datetime import timedelta


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore") # Added extra="ignore" to allow unknown fields

    DATABASE_URL: str = "sqlite:///./sql_app.db"
    SECRET_KEY: str = "your-super-secret-key-replace-me-in-production" # Used for mocking token
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALLOWED_ORIGINS: str = "http://localhost:3000"  # Default value for development

settings = Settings()