"""
German language translator.

Example:
    token=A13, counter=48 →
    "Token-Nummer A Eins Drei, Schalter-Nummer Vier Acht."
"""

from app.modules.language.translators.base import BaseTranslator
from app.shared.helpers.digit_converter import convert_to_digits


class GermanTranslator(BaseTranslator):
    """Generates German banking announcements with digit-by-digit pronunciation."""

    LANGUAGE_CODE = "de"

    def translate(self, token: str, counter: str) -> str:
        """Generate a German announcement string.

        Args:
            token: Token number string (e.g., "A13").
            counter: Counter number string (e.g., "48").

        Returns:
            Announcement string in German, e.g.
            "Token-Nummer A Eins Drei, Schalter-Nummer Vier Acht."
        """
        token_spoken = convert_to_digits(token, self.LANGUAGE_CODE)
        counter_spoken = convert_to_digits(counter, self.LANGUAGE_CODE)
        return f"Token-Nummer {token_spoken}, Schalter-Nummer {counter_spoken}."
