"""
Spanish language translator.

Example:
    token=A13, counter=48 →
    "Número de turno A Uno Tres, Número de mostrador Cuatro Ocho."
"""

from app.modules.language.translators.base import BaseTranslator
from app.shared.helpers.digit_converter import convert_to_digits


class SpanishTranslator(BaseTranslator):
    """Generates Spanish banking announcements with digit-by-digit pronunciation."""

    LANGUAGE_CODE = "es"

    def translate(self, token: str, counter: str) -> str:
        """Generate a Spanish announcement string.

        Args:
            token: Token number string (e.g., "A13").
            counter: Counter number string (e.g., "48").

        Returns:
            Announcement string in Spanish, e.g.
            "Número de turno A Uno Tres, Número de mostrador Cuatro Ocho."
        """
        token_spoken = convert_to_digits(token, self.LANGUAGE_CODE)
        counter_spoken = convert_to_digits(counter, self.LANGUAGE_CODE)
        return f"Número de turno {token_spoken}, Número de mostrador {counter_spoken}."
