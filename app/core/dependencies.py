"""
FastAPI dependency injection helpers.

Provides reusable Depends() callables for routes.
"""

from functools import lru_cache
from typing import Annotated

from fastapi import Depends

from app.core.config import Settings, get_settings

# Type alias for injecting settings via Depends
SettingsDep = Annotated[Settings, Depends(get_settings)]
