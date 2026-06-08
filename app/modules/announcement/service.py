"""
Announcement service — orchestrates translation → TTS synthesis → file storage.

This is the core business logic layer. It:
1. Validates the language code.
2. Resolves the correct language translator.
3. Translates token/counter to a spoken announcement string.
4. Resolves the Edge-TTS voice for the requested language/gender.
5. Checks disk space before synthesis.
6. Synthesizes the announcement to an MP3 file via EdgeTTSProvider.
7. Returns all data needed to build the API response.
"""

from pathlib import Path
from typing import Dict, Type

from app.core.exceptions import TTSFailureException, ValidationException
from app.core.logger import get_logger
from app.modules.announcement.schemas import AnnouncementRequest, AnnouncementResponse
from app.modules.language.translators.bangla import BanglaTranslator
from app.modules.language.translators.base import BaseTranslator
from app.modules.language.translators.english import EnglishTranslator
from app.modules.language.translators.german import GermanTranslator
from app.modules.language.translators.japanese import JapaneseTranslator
from app.modules.language.translators.spanish import SpanishTranslator
from app.modules.tts.providers.edge_tts_provider import EdgeTTSProvider
from app.shared.helpers.audio_helper import (
    check_disk_space,
    cleanup_old_files,
    generate_audio_filename,
    get_audio_url,
)
from app.shared.helpers.language_helper import resolve_voice, validate_language

logger = get_logger(__name__)

# Registry mapping language codes → translator classes
_TRANSLATOR_REGISTRY: Dict[str, Type[BaseTranslator]] = {
    "en": EnglishTranslator,
    "bn": BanglaTranslator,
    "ja": JapaneseTranslator,
    "de": GermanTranslator,
    "es": SpanishTranslator,
}


class AnnouncementService:
    """Orchestrates the full announcement generation pipeline."""

    def __init__(self, audio_dir: Path, ttl_seconds: int = 300) -> None:
        """Initialise the service.

        Args:
            audio_dir: Directory where generated MP3 files are stored.
            ttl_seconds: Maximum age of audio files before cleanup (seconds).
        """
        self._audio_dir = audio_dir
        self._ttl_seconds = ttl_seconds
        self._tts_provider = EdgeTTSProvider()

    async def generate(self, request: AnnouncementRequest) -> AnnouncementResponse:
        """Generate a TTS announcement MP3 from the request payload.

        Args:
            request: Validated announcement request.

        Returns:
            AnnouncementResponse with audio URL and metadata.

        Raises:
            ValidationException: If token/counter contain invalid characters.
            TTSFailureException: If Edge-TTS synthesis fails.
        """
        # 1. Validate inputs
        language = validate_language(request.language)
        token = request.token.strip()
        counter = request.counter.strip()

        if not token or not counter:
            raise ValidationException("Token and counter must not be empty.")

        # 2. Translate to spoken announcement
        translator_cls = _TRANSLATOR_REGISTRY.get(language, EnglishTranslator)
        translator = translator_cls()
        announcement_text = translator.translate(token=token, counter=counter)
        logger.debug("Announcement text [%s]: %s", language, announcement_text)

        # 3. Resolve voice
        voice = resolve_voice(language=language, gender=request.gender)

        # 4. Check disk space (non-fatal — log warning only)
        if not await check_disk_space(self._audio_dir):
            logger.warning("Low disk space — audio generation may fail.")

        # 5. Run background cleanup of old files (fire-and-forget style)
        await cleanup_old_files(self._audio_dir, self._ttl_seconds)

        # 6. Generate unique filename and synthesize
        filename = generate_audio_filename()
        output_path = self._audio_dir / filename

        await self._tts_provider.synthesize(
            text=announcement_text,
            voice=voice,
            output_path=output_path,
            rate=request.rate,
            pitch=request.pitch,
            volume=request.volume,
        )

        # 7. Build response
        audio_url = get_audio_url(filename)
        return AnnouncementResponse(
            token=token,
            counter=counter,
            language=language,
            voice=voice,
            announcement_text=announcement_text,
            audio_url=audio_url,
            filename=filename,
        )
