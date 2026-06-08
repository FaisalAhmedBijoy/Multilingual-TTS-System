"""
Japanese language translator.

Example:
    token=A13, counter=48 →
    "トークン番号 エー 一 三、カウンター番号 四 八。"
"""

from app.modules.language.translators.base import BaseTranslator
from app.shared.helpers.digit_converter import convert_to_digits


class JapaneseTranslator(BaseTranslator):
    """Generates Japanese banking announcements with digit-by-digit pronunciation."""

    LANGUAGE_CODE = "ja"

    def translate(self, token: str, counter: str) -> str:
        """Generate a Japanese announcement string.

        Args:
            token: Token number string (e.g., "A13").
            counter: Counter number string (e.g., "48").

        Returns:
            Announcement string in Japanese, e.g.
            "トークン番号 エー 一 三、カウンター番号 四 八。"
        """
        token_spoken = convert_to_digits(token, self.LANGUAGE_CODE)
        counter_spoken = convert_to_digits(counter, self.LANGUAGE_CODE)
        return f"トークン番号 {token_spoken}、カウンター番号 {counter_spoken}。"
