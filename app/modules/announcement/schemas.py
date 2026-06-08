"""
Pydantic schemas for the announcement module.

Defines request and response models for the POST /api/v1/announcements endpoint.
"""

from typing import Literal, Optional

from pydantic import BaseModel, Field, field_validator

from app.core.constants import LANGUAGES


class AnnouncementRequest(BaseModel):
    """Request payload for generating a TTS announcement."""

    token: str = Field(
        ...,
        min_length=1,
        max_length=20,
        description="Token/queue number to announce (e.g. 'A13').",
        examples=["A13", "B04", "125"],
    )
    counter: str = Field(
        ...,
        min_length=1,
        max_length=10,
        description="Counter/window number to announce (e.g. '5').",
        examples=["5", "12"],
    )
    language: str = Field(
        default="en",
        description="ISO 639-1 language code. Supported: en, bn, ja, de, es.",
        examples=["en", "bn", "ja", "de", "es"],
    )
    gender: Literal["male", "female"] = Field(
        default="female",
        description="Voice gender to use for synthesis.",
    )
    rate: float = Field(
        default=1.0,
        ge=0.5,
        le=2.0,
        description="Speech rate multiplier (0.5 = half speed, 2.0 = double speed).",
    )
    pitch: int = Field(
        default=0,
        ge=-10,
        le=10,
        description="Pitch offset in Hz (-10 to +10).",
    )
    volume: float = Field(
        default=1.0,
        ge=0.1,
        le=1.0,
        description="Volume level (0.1 = very quiet, 1.0 = full volume).",
    )

    @field_validator("language")
    @classmethod
    def validate_language_code(cls, v: str) -> str:
        """Ensure the provided language code is supported."""
        code = v.lower().strip()
        if code not in LANGUAGES:
            supported = ", ".join(sorted(LANGUAGES.keys()))
            raise ValueError(f"Unsupported language '{v}'. Supported: {supported}.")
        return code


class AnnouncementResponse(BaseModel):
    """Response payload returned after successful TTS generation."""

    token: str = Field(description="The token number that was announced.")
    counter: str = Field(description="The counter number that was announced.")
    language: str = Field(description="ISO 639-1 language code used.")
    voice: str = Field(description="Edge-TTS voice identifier used.")
    announcement_text: str = Field(description="The full announcement text that was synthesized.")
    audio_url: str = Field(description="Relative URL to stream/download the generated MP3.")
    filename: str = Field(description="Filename of the generated MP3.")
