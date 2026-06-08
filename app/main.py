"""
Banking TTS System — FastAPI application entry point.

Startup:
    uvicorn app.main:app --reload

Or directly:
    python -m app.main
"""

from contextlib import asynccontextmanager
from pathlib import Path
from typing import AsyncIterator

import uvicorn
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from app.core.config import get_settings
from app.core.exceptions import BankingTTSException
from app.core.logger import get_logger, setup_logging
from app.modules.announcement.router import router as announcement_router
from app.modules.announcement.service import AnnouncementService
from app.modules.health.router import router as health_router
from app.modules.voice.router import router as voice_router
from app.shared.middleware.cors import add_cors_middleware
from app.shared.middleware.logging_middleware import RequestLoggingMiddleware
from app.shared.middleware.security_headers import SecurityHeadersMiddleware
from app.shared.responses.base import error_response

settings = get_settings()
setup_logging(debug=settings.DEBUG, log_level=settings.LOG_LEVEL)
logger = get_logger(__name__)


# ---------------------------------------------------------------------------
# Lifespan — startup / shutdown
# ---------------------------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Application lifespan: create directories and wire up services on startup."""
    # Ensure audio output directory exists
    audio_dir = Path(settings.AUDIO_OUTPUT_DIR)
    audio_dir.mkdir(parents=True, exist_ok=True)
    logger.info("Audio output directory ready: %s", audio_dir.resolve())

    # Attach services to app state
    app.state.announcement_service = AnnouncementService(
        audio_dir=audio_dir,
        ttl_seconds=settings.AUDIO_TTL_SECONDS,
    )

    logger.info(
        "🚀 %s v%s started on http://%s:%d",
        settings.APP_NAME,
        settings.APP_VERSION,
        settings.HOST,
        settings.PORT,
    )
    yield
    logger.info("🛑 %s shutting down.", settings.APP_NAME)


# ---------------------------------------------------------------------------
# Application factory
# ---------------------------------------------------------------------------

def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description=(
            "A multilingual banking queue announcement system powered by Microsoft Edge-TTS. "
            "Supports English, Bangla, Japanese, German, and Spanish."
        ),
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
    )

    # ── Middleware (outermost middleware added last) ──────────────────────────
    add_cors_middleware(app, settings)
    app.add_middleware(RequestLoggingMiddleware)
    app.add_middleware(SecurityHeadersMiddleware)

    # ── Static files ─────────────────────────────────────────────────────────
    # Use an absolute path anchored to this file so the app works regardless
    # of the CWD when uvicorn is started (e.g. from the project root).
    _static_dir = Path(__file__).resolve().parent / "static"
    _static_dir.joinpath("generated_audio").mkdir(parents=True, exist_ok=True)
    app.mount("/static", StaticFiles(directory=str(_static_dir)), name="static")

    # ── Root page ─────────────────────────────────────────────────────────────
    @app.get("/", response_class=HTMLResponse, include_in_schema=False)
    async def index() -> HTMLResponse:
        """Serve the static landing page at the application root."""
        html_path = _static_dir / "index.html"
        return HTMLResponse(content=html_path.read_text(encoding="utf-8"))

    # ── Routers ──────────────────────────────────────────────────────────────
    app.include_router(health_router)
    app.include_router(voice_router)
    app.include_router(announcement_router)

    # ── Exception handlers ────────────────────────────────────────────────────
    @app.exception_handler(BankingTTSException)
    async def banking_tts_exception_handler(
        request: Request, exc: BankingTTSException
    ) -> JSONResponse:
        logger.error("BankingTTSException [%s]: %s", exc.error_code, exc.message)
        return JSONResponse(
            status_code=exc.status_code,
            content=error_response(code=exc.error_code, message=exc.message),
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        errors = exc.errors()
        message = "; ".join(
            f"{' → '.join(str(loc) for loc in e['loc'])}: {e['msg']}"
            for e in errors
        )
        logger.warning("Request validation failed: %s", message)
        return JSONResponse(
            status_code=422,
            content=error_response(code="VALIDATION_ERROR", message=message),
        )

    @app.exception_handler(Exception)
    async def generic_exception_handler(
        request: Request, exc: Exception
    ) -> JSONResponse:
        logger.error("Unhandled exception: %s", exc, exc_info=True)
        return JSONResponse(
            status_code=500,
            content=error_response(
                code="INTERNAL_ERROR",
                message="An unexpected error occurred. Please try again.",
            ),
        )

    return app


app = create_app()


# ---------------------------------------------------------------------------
# Direct execution
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
    )
