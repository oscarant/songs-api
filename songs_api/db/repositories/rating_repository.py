import asyncio
from dataclasses import dataclass
from typing import Any, Dict, List, Tuple

from beanie import PydanticObjectId

from songs_api.db.models.rating import Rating


@dataclass
class RatingRepository:
    """Handles persistence of ratings and computing statistics."""

    def add_rating(self, song_id: str, rating_value: int) -> Rating:
        """
        Insert a new Rating document and return it.

        Raises:
          ValueError: if `song_id` is invalid.
        """
        try:
            obj_id = PydanticObjectId(song_id)
        except Exception:
            raise ValueError(f"Invalid song_id: {song_id}") from None

        rating = Rating(song_id=obj_id, rating=rating_value)
        return self._run_async(rating.insert())

    def get_rating_stats(self, song_id: str) -> Tuple[float, int, int]:
        """
        Compute average, minimum, and maximum rating for a given song.

        Raises:
          ValueError: if `song_id` is invalid.

        Returns:
          (average: float, lowest: int, highest: int)
        """
        try:
            obj_id = PydanticObjectId(song_id)
        except Exception:
            raise ValueError(f"Invalid song_id: {song_id}") from None

        pipeline: List[Dict[str, Any]] = [
            {"$match": {"song_id": obj_id}},
            {
                "$group": {
                    "_id": None,
                    "avg": {"$avg": "$rating"},
                    "min": {"$min": "$rating"},
                    "max": {"$max": "$rating"},
                },
            },
        ]
        cursor = Rating.get_motor_collection().aggregate(pipeline)
        result = self._run_async(cursor.to_list(length=1))
        if not result:
            return 0.0, 0, 0

        stats = result[0]
        return stats.get("avg", 0.0), stats.get("min", 0), stats.get("max", 0)

    def _run_async(self, coro: Any) -> Any:
        """Helper method to run async code in a synchronous context."""
        loop = asyncio.new_event_loop()
        try:
            return loop.run_until_complete(coro)
        finally:
            loop.close()


# Module-level singleton for convenience
rating_repo = RatingRepository()
