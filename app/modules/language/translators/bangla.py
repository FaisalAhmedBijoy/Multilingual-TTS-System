"""
Bangla language translator.

Example:
    token=A13, counter=48 →
    "টোকেন নম্বর এ এক তিন, কাউন্টার নম্বর চার আট।"
"""

from app.modules.language.translators.base import BaseTranslator
from app.shared.helpers.digit_converter import convert_to_digits


class BanglaTranslator(BaseTranslator):
    """Generates Bangla banking announcements with digit-by-digit pronunciation."""

    LANGUAGE_CODE = "bn"

    def translate(self, token: str, counter: str) -> str:
        """Generate a Bangla announcement string.

        Args:
            token: Token number string (e.g., "A13").
            counter: Counter number string (e.g., "48").

        Returns:
            Announcement string in Bangla, e.g.
            "টোকেন নম্বর এ এক তিন, কাউন্টার নম্বর চার আট।"
        """
        token_spoken = convert_to_digits(token, self.LANGUAGE_CODE)
        counter_spoken = convert_to_digits(counter, self.LANGUAGE_CODE)
        return f"টোকেন নম্বর {token_spoken}, কাউন্টার নম্বর {counter_spoken}।"
