"""
Health check router — GET /health

Returns application status, version, and uptime.
"""

import time

from fastapi import APIRouter

from app.core.config import get_settings
from app.shared.responses.base import success_response

router = APIRouter(tags=["Health"])

_start_time = time.time()


@router.get(
    "/health",
    summary="Application health check",
    description="Returns application name, version, status, and uptime in seconds.",
)
async def health_check() -> dict:
    """Return the application health status.

    Returns:
        Standard success envelope containing health metadata.
    """
    settings = get_settings()
    uptime_seconds = round(time.time() - _start_time, 2)
    return success_response(
        {
            "status": "ok",
            "app": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "uptime_seconds": uptime_seconds,
        }
    )
