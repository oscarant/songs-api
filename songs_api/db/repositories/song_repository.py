import asyncio
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from beanie import PydanticObjectId

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

        total = self._run_async(Song.find().count())
        items = self._run_async(Song.find().skip(skip).limit(size).to_list())
        return items, total

    def average_difficulty(self, level: Optional[int] = None) -> float:
        """
        Compute the average difficulty across all songs, optionally filtered by level.

        Args:
            level: Optional level to filter songs by difficulty.
        Returns:
            Average difficulty as a float.
        """
        pipeline: List[Dict[str, Any]] = []
        if level is not None:
            pipeline.append({"$match": {"level": level}})
        pipeline.append({"$group": {"_id": None, "avg": {"$avg": "$difficulty"}}})
        cursor = Song.get_motor_collection().aggregate(pipeline)
        result = self._run_async(cursor.to_list(length=1))
        return result[0]["avg"] if result else 0.0

    def search_songs(self, message: str) -> List[Song]:
        """Perform case-insensitive text search on artist and title."""
        # Use MongoDB text index
        cursor = Song.find({"$text": {"$search": message}})
        return self._run_async(cursor.to_list())

    def get_song_by_id(self, song_id: str) -> Song:
        """Fetch a single song; raises ValueError if not found."""
        try:
            obj_id = PydanticObjectId(song_id)
        except Exception:
            raise ValueError(f"Invalid song_id: {song_id}") from None

        song = self._run_async(Song.get(obj_id))
        if not song:
            raise ValueError(f"Song not found: {song_id}") from None
        return song

    def _run_async(self, coro: Any) -> Any:
        """Helper method to run async code in a synchronous context."""
        loop = asyncio.new_event_loop()
        try:
            return loop.run_until_complete(coro)
        finally:
            loop.close()
