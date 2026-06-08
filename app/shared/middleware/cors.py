"""
CORS middleware configuration.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import Settings


def add_cors_middleware(app: FastAPI, settings: Settings) -> None:
    """Add CORS middleware to the FastAPI application.

    Args:
        app: The FastAPI application instance.
        settings: Application settings containing allowed origins.
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
