"""
Abstract base class for all language translators.
"""

from abc import ABC, abstractmethod


class BaseTranslator(ABC):
    """Abstract translator that converts token/counter to an announcement string.

    Subclasses implement :meth:`translate` for each supported language.
    """

    @abstractmethod
    def translate(self, token: str, counter: str) -> str:
        """Generate a spoken announcement string for the given token/counter.

        Args:
            token: Token number string (e.g., "A13").
            counter: Counter number string (e.g., "48").

        Returns:
            Full announcement text in the target language, with digit-by-digit
            pronunciation for all digits and letters.
        """
        ...
