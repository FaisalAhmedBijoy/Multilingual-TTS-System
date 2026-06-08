"""
Core digit-by-digit converter.

Converts each character of a token/counter string into its spoken-word
equivalent for the given language, joined by spaces.
"""

from app.core.constants import BN_LETTERS, DIGIT_MAPS, JA_LETTERS
from app.core.logger import get_logger

logger = get_logger(__name__)


def convert_to_digits(text: str, language: str) -> str:
    """Convert each character of *text* to its spoken-word form.

    Rules:
    - Digit characters (0-9) → language-specific spoken word.
    - Alpha characters (A-Z) → kept as-is for EN/DE/ES; transliterated
      to Katakana for JA, and to Bangla for BN.
    - Hyphens and spaces are ignored (collapsed).

    Args:
        text: Input string (token or counter number), e.g. "A13".
        language: ISO 639-1 language code ("en", "bn", "ja", "de", "es").

    Returns:
        Space-separated spoken-word string, e.g. "A One Three".
    """
    digit_map = DIGIT_MAPS.get(language, DIGIT_MAPS["en"])
    parts: list[str] = []

    for char in text.upper():
        if char.isdigit():
            parts.append(digit_map.get(char, char))
        elif char.isalpha():
            if language == "bn":
                parts.append(BN_LETTERS.get(char, char))
            elif language == "ja":
                parts.append(JA_LETTERS.get(char, char))
            else:
                # EN, DE, ES — keep the letter; TTS engine will pronounce it
                parts.append(char)
        # Skip spaces, hyphens, and other punctuation

    result = " ".join(parts)
    logger.debug("convert_to_digits: '%s' (%s) → '%s'", text, language, result)
    return result
