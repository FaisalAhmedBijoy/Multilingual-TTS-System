"""
Application configuration using pydantic-settings.

Loads settings from environment variables and .env file.
"""

from functools import lru_cache
from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables / .env file."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Application
    APP_NAME: str = Field(default="Banking TTS System")
    APP_VERSION: str = Field(default="1.0.0")
    DEBUG: bool = Field(default=False)

    # Server
    HOST: str = Field(default="0.0.0.0")
    PORT: int = Field(default=8000)

    # CORS
    ALLOWED_ORIGINS: List[str] = Field(
        default=["http://localhost:8000", "http://localhost:3000"]
    )

    # Audio
    AUDIO_OUTPUT_DIR: str = Field(default="static/generated_audio")
    AUDIO_TTL_SECONDS: int = Field(default=300)

    # TTS Defaults
    DEFAULT_VOICE_GENDER: str = Field(default="female")
    DEFAULT_SPEECH_RATE: float = Field(default=1.0)
    DEFAULT_PITCH: int = Field(default=0)
    DEFAULT_VOLUME: float = Field(default=1.0)

    # Logging
    LOG_LEVEL: str = Field(default="INFO")

    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = Field(default=30)


@lru_cache()
def get_settings() -> Settings:
    """Return cached Settings instance.

    Returns:
        Settings: Application settings singleton.
    """
    return Settings()
