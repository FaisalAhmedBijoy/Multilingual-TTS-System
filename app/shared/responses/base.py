"""
Standardized API response wrappers.

All endpoints return either success_response() or error_response() to ensure
consistent JSON structure across the entire API.
"""

from typing import Any, Dict


def success_response(data: Any) -> Dict[str, Any]:
    """Wrap data in a standard success response envelope.

    Args:
        data: The payload to include under the "data" key.

    Returns:
        Dict with {"success": True, "data": data}.
    """
    return {"success": True, "data": data}


def error_response(code: str, message: str) -> Dict[str, Any]:
    """Wrap an error in a standard error response envelope.

    Args:
        code: Machine-readable error code string.
        message: Human-readable error message.

    Returns:
        Dict with {"success": False, "error": {"code": ..., "message": ...}}.
    """
    return {
        "success": False,
        "error": {
            "code": code,
            "message": message,
        },
    }
