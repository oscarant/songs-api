import asyncio
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from bson import ObjectId

from songs_api.config import Settings
from songs_api.db.models.song import Song



@dataclass
class SongRepository:
    settings: Settings = field(default_factory=Settings)

    def list_songs(
        self,
        page: int = 1,
        size: Optional[int] = None,
    ) -> tuple[List[Song], int]:
        """
        Return a page of songs and total count.

        Args:
          page: 1-based page number
          size: number of items per page
        """
        # Enforce max page size
        size = size or self.settings.PAGE_SIZE_DEFAULT
        size = min(size, self.settings.PAGE_SIZE_MAX)
        skip = (page - 1) * size

        songs = Song.objects.skip(skip).limit(size)
        total = Song.objects.count()
        return list(songs), total

    def average_difficulty(self, level: Optional[int] = None) -> float:
        """
        Compute the average difficulty, optionally filtered by level.
        """
        pipeline: List[Dict[str, Any]] = []

        if level is not None:
            pipeline.append({"$match": {"level": level}})

        pipeline.append({"$group": {"_id": None, "avg": {"$avg": "$difficulty"}}})

        result = Song.objects.aggregate(*pipeline)

        try:
            # Get the first result
            return next(result)["avg"]
        except (StopIteration, KeyError):
            return 0.0

    def search_songs(self, message: str) -> List[Song]:
        """Perform case-insensitive text search on artist and title."""
        # Use MongoDB text index
        return list(Song.objects.search_text(message))

    def get_song_by_id(self, song_id: str) -> Song:
        """Fetch a single song; raises ValueError if not found."""
        try:
            obj_id = ObjectId(song_id)
        except Exception:
            raise ValueError(f"Invalid song_id: {song_id}") from None

        song = Song.objects.get(id=obj_id)
        if not song:
            raise ValueError(f"Song not found: {song_id}") from None
        return song

