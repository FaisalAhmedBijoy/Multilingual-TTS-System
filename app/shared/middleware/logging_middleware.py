"""
Request/Response logging middleware.

Logs HTTP method, path, status code, and duration for every request.
"""

import time

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.core.logger import get_logger

logger = get_logger(__name__)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Logs each incoming HTTP request with timing information."""

    async def dispatch(self, request: Request, call_next: any) -> Response:
        """Process request, log timing, and pass through to next middleware.

        Args:
            request: Incoming HTTP request.
            call_next: Next middleware or route handler in the chain.

        Returns:
            HTTP response from the downstream handler.
        """
        start_time = time.perf_counter()
        response = await call_next(request)
        duration_ms = round((time.perf_counter() - start_time) * 1000, 2)

        logger.info(
            "%s %s → %d [%.2fms]",
            request.method,
            request.url.path,
            response.status_code,
            duration_ms,
        )
        return response
