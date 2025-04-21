from functools import lru_cache
from typing import Any

from motor.motor_asyncio import AsyncIOMotorClient

from songs_api.config import Settings


@lru_cache(maxsize=1)
def get_client() -> AsyncIOMotorClient[Any]:
    """Return a singleton Mongo client."""
    settings = Settings()
    return AsyncIOMotorClient(settings.MONGO_URI)
