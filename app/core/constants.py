"""
Application-wide constants.

Contains language definitions, voice mappings, and digit pronunciation maps
for all supported languages.
"""

from typing import Dict

# ---------------------------------------------------------------------------
# Supported Languages
# ---------------------------------------------------------------------------

LANGUAGES: Dict[str, Dict[str, str]] = {
    "en": {
        "name": "English",
        "voice_female": "en-US-AriaNeural",
        "voice_male": "en-US-GuyNeural",
    },
    "bn": {
        "name": "Bangla",
        "voice_female": "bn-BD-NabanitaNeural",
        "voice_male": "bn-BD-PradeepNeural",
    },
    "ja": {
        "name": "Japanese",
        "voice_female": "ja-JP-NanamiNeural",
        "voice_male": "ja-JP-KeitaNeural",
    },
    "de": {
        "name": "German",
        "voice_female": "de-DE-KatjaNeural",
        "voice_male": "de-DE-ConradNeural",
    },
    "es": {
        "name": "Spanish",
        "voice_female": "es-ES-ElviraNeural",
        "voice_male": "es-ES-AlvaroNeural",
    },
}

# ---------------------------------------------------------------------------
# Digit Maps — each language maps "0"–"9" to its spoken-word equivalent
# ---------------------------------------------------------------------------

EN_DIGITS: Dict[str, str] = {
    "0": "Zero",
    "1": "One",
    "2": "Two",
    "3": "Three",
    "4": "Four",
    "5": "Five",
    "6": "Six",
    "7": "Seven",
    "8": "Eight",
    "9": "Nine",
}

BN_DIGITS: Dict[str, str] = {
    "0": "শূন্য",
    "1": "এক",
    "2": "দুই",
    "3": "তিন",
    "4": "চার",
    "5": "পাঁচ",
    "6": "ছয়",
    "7": "সাত",
    "8": "আট",
    "9": "নয়",
}

JA_DIGITS: Dict[str, str] = {
    "0": "ゼロ",
    "1": "一",
    "2": "二",
    "3": "三",
    "4": "四",
    "5": "五",
    "6": "六",
    "7": "七",
    "8": "八",
    "9": "九",
}

DE_DIGITS: Dict[str, str] = {
    "0": "Null",
    "1": "Eins",
    "2": "Zwei",
    "3": "Drei",
    "4": "Vier",
    "5": "Fünf",
    "6": "Sechs",
    "7": "Sieben",
    "8": "Acht",
    "9": "Neun",
}

ES_DIGITS: Dict[str, str] = {
    "0": "Cero",
    "1": "Uno",
    "2": "Dos",
    "3": "Tres",
    "4": "Cuatro",
    "5": "Cinco",
    "6": "Seis",
    "7": "Siete",
    "8": "Ocho",
    "9": "Nueve",
}

# ---------------------------------------------------------------------------
# Language → digit map resolution
# ---------------------------------------------------------------------------

DIGIT_MAPS: Dict[str, Dict[str, str]] = {
    "en": EN_DIGITS,
    "bn": BN_DIGITS,
    "ja": JA_DIGITS,
    "de": DE_DIGITS,
    "es": ES_DIGITS,
}

# ---------------------------------------------------------------------------
# Bangla letter map — for alphabetic characters in token numbers
# ---------------------------------------------------------------------------

BN_LETTERS: Dict[str, str] = {
    "A": "এ",
    "B": "বি",
    "C": "সি",
    "D": "ডি",
    "E": "ই",
    "F": "এফ",
    "G": "জি",
    "H": "এইচ",
    "I": "আই",
    "J": "জে",
    "K": "কে",
    "L": "এল",
    "M": "এম",
    "N": "এন",
    "O": "ও",
    "P": "পি",
    "Q": "কিউ",
    "R": "আর",
    "S": "এস",
    "T": "টি",
    "U": "ইউ",
    "V": "ভি",
    "W": "ডাবলিউ",
    "X": "এক্স",
    "Y": "ওয়াই",
    "Z": "জেড",
}

# ---------------------------------------------------------------------------
# Japanese letter map — Roman letters spoken in katakana context
# ---------------------------------------------------------------------------

JA_LETTERS: Dict[str, str] = {
    "A": "エー",
    "B": "ビー",
    "C": "シー",
    "D": "ディー",
    "E": "イー",
    "F": "エフ",
    "G": "ジー",
    "H": "エイチ",
    "I": "アイ",
    "J": "ジェー",
    "K": "ケー",
    "L": "エル",
    "M": "エム",
    "N": "エヌ",
    "O": "オー",
    "P": "ピー",
    "Q": "キュー",
    "R": "アール",
    "S": "エス",
    "T": "ティー",
    "U": "ユー",
    "V": "ブイ",
    "W": "ダブリュー",
    "X": "エックス",
    "Y": "ワイ",
    "Z": "ゼット",
}

# ---------------------------------------------------------------------------
# Error codes
# ---------------------------------------------------------------------------

ERR_VALIDATION_ERROR = "VALIDATION_ERROR"
ERR_UNSUPPORTED_LANGUAGE = "UNSUPPORTED_LANGUAGE"
ERR_TTS_FAILURE = "TTS_FAILURE"
ERR_AUDIO_WRITE_FAILURE = "AUDIO_WRITE_FAILURE"
ERR_RATE_LIMIT_EXCEEDED = "RATE_LIMIT_EXCEEDED"
ERR_INTERNAL = "INTERNAL_ERROR"

# ---------------------------------------------------------------------------
# Misc
# ---------------------------------------------------------------------------

AUDIO_MIME_TYPE = "audio/mpeg"
MIN_DISK_SPACE_MB = 50
STATIC_AUDIO_URL_PREFIX = "/static/generated_audio"
