"""
Edge-TTS provider — wraps the edge_tts library for async audio synthesis.

Writes synthesized MP3 audio to a given output path using the SSML built
by the ssml_builder helper.
"""

from pathlib import Path

import edge_tts

from app.core.exceptions import TTSFailureException
from app.core.logger import get_logger
from app.shared.helpers.ssml_builder import build_ssml

logger = get_logger(__name__)


class EdgeTTSProvider:
    """Synthesizes speech using Microsoft Edge-TTS (edge_tts library)."""

    async def synthesize(
        self,
        text: str,
        voice: str,
        output_path: Path,
        rate: float = 1.0,
        pitch: int = 0,
        volume: float = 1.0,
    ) -> None:
        """Synthesize *text* with Edge-TTS and write the MP3 to *output_path*.

        Args:
            text: The announcement text to synthesize.
            voice: Edge-TTS voice identifier (e.g. ``"en-US-AriaNeural"``).
            output_path: Destination path for the generated MP3 file.
            rate: Speech rate multiplier (0.5–2.0). Defaults to 1.0.
            pitch: Pitch offset in Hz (-10 to +10). Defaults to 0.
            volume: Volume level (0.1–1.0). Defaults to 1.0.

        Raises:
            TTSFailureException: If Edge-TTS synthesis or file write fails.
        """
        ssml = build_ssml(text=text, voice=voice, rate=rate, pitch=pitch, volume=volume)
        logger.debug("Synthesizing via Edge-TTS: voice=%s, output=%s", voice, output_path)

        try:
            communicate = edge_tts.Communicate(ssml, voice, ssml=True)
            await communicate.save(str(output_path))
            logger.info("Audio saved: %s", output_path.name)
        except Exception as exc:
            logger.error("Edge-TTS synthesis failed: %s", exc, exc_info=True)
            raise TTSFailureException(f"Edge-TTS synthesis failed: {exc}") from exc
