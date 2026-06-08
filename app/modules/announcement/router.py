"""
Announcement router — POST /api/v1/announcements

Accepts token/counter data and returns a generated MP3 audio URL.
"""

from fastapi import APIRouter, Request

from app.core.exceptions import BankingTTSException
from app.core.logger import get_logger
from app.modules.announcement.schemas import AnnouncementRequest, AnnouncementResponse
from app.shared.responses.base import error_response, success_response

logger = get_logger(__name__)

router = APIRouter(prefix="/api/v1/announcements", tags=["Announcements"])


@router.post(
    "",
    summary="Generate a multilingual banking announcement",
    description=(
        "Converts a token number and counter number into a spoken MP3 announcement "
        "in the requested language. Returns the audio URL and announcement metadata."
    ),
    response_description="Success response containing announcement metadata and audio URL.",
)
async def create_announcement(
    payload: AnnouncementRequest,
    request: Request,
) -> dict:
    """Generate a TTS announcement MP3 and return its public audio URL.

    Args:
        payload: Announcement request containing token, counter, language, and voice settings.
        request: FastAPI request object (used to access the service from app state).

    Returns:
        Standard success envelope containing AnnouncementResponse data.
    """
    service = request.app.state.announcement_service
    try:
        result: AnnouncementResponse = await service.generate(payload)
        return success_response(result.model_dump())
    except BankingTTSException as exc:
        logger.error("Announcement generation failed: %s", exc.message)
        return error_response(code=exc.error_code, message=exc.message)
