"""
Language code validation and voice resolution helpers.
"""

from typing import Literal

from app.core.constants import LANGUAGES
from app.core.exceptions import UnsupportedLanguageException
from app.core.logger import get_logger

logger = get_logger(__name__)

VoiceGender = Literal["male", "female"]


def validate_language(language: str) -> str:
    """Validate that a language code is supported.

    Args:
        language: ISO 639-1 language code to validate.

    Returns:
        The validated language code (lowercased).

    Raises:
        UnsupportedLanguageException: If the language code is not in LANGUAGES.
    """
    code = language.lower().strip()
    if code not in LANGUAGES:
        raise UnsupportedLanguageException(language)
    return code


def resolve_voice(language: str, gender: VoiceGender) -> str:
    """Resolve the Edge-TTS voice ID for a language/gender combination.

    Args:
        language: Validated ISO 639-1 language code.
        gender: "male" or "female".

    Returns:
        Edge-TTS voice identifier string.

    Raises:
        UnsupportedLanguageException: If the language code is not supported.
    """
    lang_data = LANGUAGES.get(language)
    if not lang_data:
        raise UnsupportedLanguageException(language)

    key = f"voice_{gender}"
    voice = lang_data.get(key, lang_data["voice_female"])
    logger.debug("Resolved voice: lang=%s, gender=%s → %s", language, gender, voice)
    return voice
