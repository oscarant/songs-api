from functools import lru_cache

import mongoengine

from songs_api.config import Settings


@lru_cache(maxsize=1)
def connect_db() -> None:
    """Connect to MongoDB using MongoEngine."""
    settings = Settings()
    mongoengine.connect(host=settings.MONGO_URI)
