"""
SSML markup builder for Edge-TTS.

Builds complete SSML strings with prosody controls for rate, pitch, and volume.
"""


def _rate_to_ssml(rate: float) -> str:
    """Convert a rate multiplier to an Edge-TTS SSML percentage string.

    Examples:
        1.0 → "+0%"
        1.2 → "+20%"
        0.8 → "-20%"

    Args:
        rate: Speech rate multiplier (0.5–2.0).

    Returns:
        SSML-formatted rate string.
    """
    percentage = round((rate - 1.0) * 100)
    sign = "+" if percentage >= 0 else ""
    return f"{sign}{percentage}%"


def _pitch_to_ssml(pitch: int) -> str:
    """Convert an integer pitch offset to an Edge-TTS SSML Hz string.

    Examples:
        0  → "+0Hz"
        5  → "+5Hz"
        -3 → "-3Hz"

    Args:
        pitch: Pitch offset in Hz (-10 to +10).

    Returns:
        SSML-formatted pitch string.
    """
    sign = "+" if pitch >= 0 else ""
    return f"{sign}{pitch}Hz"


def _volume_to_ssml(volume: float) -> str:
    """Convert a volume float to an Edge-TTS SSML percentage string.

    Examples:
        1.0 → "+0%"
        0.5 → "-50%"

    Args:
        volume: Volume level (0.1–1.0).

    Returns:
        SSML-formatted volume string.
    """
    percentage = round((volume - 1.0) * 100)
    sign = "+" if percentage >= 0 else ""
    return f"{sign}{percentage}%"


def build_ssml(
    text: str,
    voice: str,
    rate: float,
    pitch: int,
    volume: float,
) -> str:
    """Build a complete SSML document for Edge-TTS synthesis.

    Args:
        text: The announcement text to synthesize.
        voice: Edge-TTS voice identifier (e.g., "en-US-AriaNeural").
        rate: Speech rate multiplier (0.5–2.0).
        pitch: Pitch offset in Hz (-10 to +10).
        volume: Volume level (0.1–1.0).

    Returns:
        Complete SSML XML string ready for Edge-TTS Communicate.
    """
    rate_str = _rate_to_ssml(rate)
    pitch_str = _pitch_to_ssml(pitch)
    volume_str = _volume_to_ssml(volume)

    # Escape XML special characters in text
    safe_text = (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&apos;")
    )

    ssml = (
        f'<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" '
        f'xml:lang="en-US">'
        f'<voice name="{voice}">'
        f'<prosody rate="{rate_str}" pitch="{pitch_str}" volume="{volume_str}">'
        f"{safe_text}"
        f"</prosody>"
        f"</voice>"
        f"</speak>"
    )
    return ssml
