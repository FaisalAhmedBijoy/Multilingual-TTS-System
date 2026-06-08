"""
English language translator.

Example:
    token=A13, counter=48 →
    "Token Number A One Three, Counter Number Four Eight."
"""

from app.modules.language.translators.base import BaseTranslator
from app.shared.helpers.digit_converter import convert_to_digits


class EnglishTranslator(BaseTranslator):
    """Generates English banking announcements with digit-by-digit pronunciation."""

    LANGUAGE_CODE = "en"

    def translate(self, token: str, counter: str) -> str:
        """Generate an English announcement string.

        Args:
            token: Token number string (e.g., "A13").
            counter: Counter number string (e.g., "48").

        Returns:
            Announcement string, e.g.
            "Token Number A One Three, Counter Number Four Eight."
        """
        token_spoken = convert_to_digits(token, self.LANGUAGE_CODE)
        counter_spoken = convert_to_digits(counter, self.LANGUAGE_CODE)
        return f"Token Number {token_spoken}, Counter Number {counter_spoken}."
