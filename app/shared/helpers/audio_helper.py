"""
Audio file management helpers.

Provides UUID-based filename generation, URL resolution, async TTL-based
cleanup of old audio files, and disk space checking.
"""

import asyncio
import time
import uuid
from pathlib import Path

import aiofiles.os

from app.core.constants import MIN_DISK_SPACE_MB, STATIC_AUDIO_URL_PREFIX
from app.core.logger import get_logger

logger = get_logger(__name__)


def generate_audio_filename() -> str:
    """Generate a unique audio filename using UUID4 and Unix timestamp.

    Returns:
        Filename string in format "{uuid4_hex}_{unix_timestamp}.mp3".
    """
    uid = uuid.uuid4().hex
    ts = int(time.time())
    return f"{uid}_{ts}.mp3"


def get_audio_url(filename: str) -> str:
    """Resolve an audio filename to its public URL path.

    Args:
        filename: The MP3 filename (e.g., "abc123_1705312200.mp3").

    Returns:
        Public URL path (e.g., "/static/generated_audio/abc123_1705312200.mp3").
    """
    return f"{STATIC_AUDIO_URL_PREFIX}/{filename}"


async def cleanup_old_files(directory: Path, ttl_seconds: int) -> int:
    """Delete audio files older than *ttl_seconds* from *directory*.

    Args:
        directory: Path to the audio output directory.
        ttl_seconds: Maximum age of files in seconds before deletion.

    Returns:
        Number of files deleted.
    """
    if not directory.exists():
        return 0

    cutoff = time.time() - ttl_seconds
    deleted = 0

    try:
        entries = list(directory.iterdir())
    except OSError as exc:
        logger.error("Failed to list audio directory: %s", exc)
        return 0

    for entry in entries:
        if not entry.is_file() or not entry.suffix == ".mp3":
            continue
        try:
            stat = await aiofiles.os.stat(entry)
            if stat.st_mtime < cutoff:
                await aiofiles.os.remove(entry)
                deleted += 1
                logger.debug("Deleted old audio file: %s", entry.name)
        except OSError as exc:
            logger.warning("Could not delete audio file %s: %s", entry.name, exc)

    if deleted:
        logger.debug("Audio cleanup complete: %d file(s) deleted", deleted)

    return deleted


async def check_disk_space(directory: Path, min_mb: int = MIN_DISK_SPACE_MB) -> bool:
    """Check whether sufficient disk space is available.

    Args:
        directory: Path to check disk space for.
        min_mb: Minimum required free space in megabytes.

    Returns:
        True if free space >= min_mb, False otherwise.
    """
    try:
        loop = asyncio.get_event_loop()
        stat = await loop.run_in_executor(None, lambda: Path(directory).stat())
        # Use shutil.disk_usage for accurate free space
        import shutil
        usage = await loop.run_in_executor(None, shutil.disk_usage, str(directory))
        free_mb = usage.free / (1024 * 1024)
        return free_mb >= min_mb
    except OSError as exc:
        logger.error("Disk space check failed: %s", exc)
        return False
