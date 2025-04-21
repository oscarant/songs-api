from typing import Any, Dict, List, Optional, Tuple

from beanie import PydanticObjectId

from songs_api.config import Settings
from songs_api.db.models.song import Song

settings = Settings()


async def list_songs(
    page: int = 1,
    size: int = settings.PAGE_SIZE_DEFAULT,
) -> Tuple[List[Song], int]:
    """
    Return a page of songs and total count.

    Args:
      page: 1-based page number
      size: number of items per page
    """
    # Enforce max page size
    size = min(size, settings.PAGE_SIZE_MAX)
    skip = (page - 1) * size

    total = await Song.find().count()
    items = await Song.find().skip(skip).limit(size).to_list()

    return items, total


async def average_difficulty(level: Optional[int] = None) -> float:
    """Compute the average difficulty across all songs, optionally filtered by level."""
    pipeline: List[Dict[str, Any]] = []
    if level is not None:
        pipeline.append({"$match": {"level": level}})
    pipeline.append({"$group": {"_id": None, "avg": {"$avg": "$difficulty"}}})
    cursor = Song.get_motor_collection().aggregate(pipeline)
    result = await cursor.to_list(length=1)
    return result[0]["avg"] if result else 0.0


async def search_songs(message: str) -> List[Song]:
    """Perform case-insensitive text search on artist and title."""
    # Use MongoDB text index
    cursor = Song.find({"$text": {"$search": message}})
    return await cursor.to_list()


async def get_song_by_id(song_id: str) -> Song:
    """Fetch a single song; raises ValueError if not found."""
    try:
        obj_id = PydanticObjectId(song_id)
    except Exception:
        raise ValueError(f"Invalid song_id: {song_id}") from None

    song = await Song.get(obj_id)
    if not song:
        raise ValueError(f"Song not found: {song_id}") from None
    return song
