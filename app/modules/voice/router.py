"""
Voice listing router — GET /api/v1/voices

Returns all supported languages with their available voice options.
"""

from fastapi import APIRouter

from app.core.constants import LANGUAGES
from app.shared.responses.base import success_response

router = APIRouter(prefix="/api/v1/voices", tags=["Voices"])


@router.get(
    "",
    summary="List all supported voices",
    description=(
        "Returns a list of all supported languages with their language codes, "
        "display names, and available voice identifiers for male and female genders."
    ),
)
async def list_voices() -> dict:
    """Return all supported languages and their available voices.

    Returns:
        Standard success envelope containing a list of language/voice options.
    """
    voices = [
        {
            "language_code": code,
            "language_name": data["name"],
            "voices": {
                "female": data["voice_female"],
                "male": data["voice_male"],
            },
        }
        for code, data in LANGUAGES.items()
    ]
    return success_response({"supported_languages": len(voices), "voices": voices})
