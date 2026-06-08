"""
Custom exception classes for the Banking TTS System.

All exceptions have a machine-readable error code and human-readable message.
Global exception handlers are registered in app/main.py.
"""

from app.core.constants import (
    ERR_AUDIO_WRITE_FAILURE,
    ERR_INTERNAL,
    ERR_TTS_FAILURE,
    ERR_UNSUPPORTED_LANGUAGE,
    ERR_VALIDATION_ERROR,
)


class BankingTTSException(Exception):
    """Base exception for all Banking TTS System errors.

    Attributes:
        error_code: Machine-readable error code string.
        message: Human-readable error message.
        status_code: HTTP status code to return.
    """

    def __init__(
        self,
        message: str,
        error_code: str = ERR_INTERNAL,
        status_code: int = 500,
    ) -> None:
        """Initialize the exception.

        Args:
            message: Human-readable error message.
            error_code: Machine-readable error code.
            status_code: HTTP status code to return.
        """
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        super().__init__(message)


class TTSFailureException(BankingTTSException):
    """Raised when Edge-TTS synthesis fails."""

    def __init__(self, message: str = "TTS synthesis failed.") -> None:
        """Initialize TTS failure exception.

        Args:
            message: Human-readable error message.
        """
        super().__init__(message=message, error_code=ERR_TTS_FAILURE, status_code=500)


class UnsupportedLanguageException(BankingTTSException):
    """Raised when an unsupported language code is provided."""

    def __init__(self, language: str) -> None:
        """Initialize unsupported language exception.

        Args:
            language: The unsupported language code.
        """
        super().__init__(
            message=f"Language '{language}' is not supported.",
            error_code=ERR_UNSUPPORTED_LANGUAGE,
            status_code=400,
        )


class ValidationException(BankingTTSException):
    """Raised for business-level validation failures."""

    def __init__(self, message: str) -> None:
        """Initialize validation exception.

        Args:
            message: Human-readable validation error message.
        """
        super().__init__(
            message=message,
            error_code=ERR_VALIDATION_ERROR,
            status_code=422,
        )


class AudioWriteException(BankingTTSException):
    """Raised when audio file cannot be written to disk."""

    def __init__(self, message: str = "Failed to write audio file to disk.") -> None:
        """Initialize audio write exception.

        Args:
            message: Human-readable error message.
        """
        super().__init__(
            message=message,
            error_code=ERR_AUDIO_WRITE_FAILURE,
            status_code=500,
        )
