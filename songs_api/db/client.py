from functools import lru_cache
from typing import Optional

import mongoengine

from songs_api.config import settings


@lru_cache(maxsize=1)
def connect_db(alias: str = "default") -> None:
    """Connect to MongoDB using MongoEngine.

    Args:
        alias: Database connection alias. Default is 'default'.
    """
    mongoengine.connect(host=settings.MONGO_URI, alias=alias)


def disconnect_db(alias: Optional[str] = None) -> None:
    """Disconnect from MongoDB.

    Args:
        alias: Database connection alias. If None, disconnects all connections.
    """
    mongoengine.disconnect(alias=alias)


def get_db(alias: str = "default") -> mongoengine.Document:
    """Get the current MongoDB connection.

    Args:
        alias: Database connection alias. Default is 'default'.
    """
    return mongoengine.connection.get_db(alias=alias)
