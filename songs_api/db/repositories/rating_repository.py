import asyncio
from dataclasses import dataclass
from typing import Any, Dict, List, Tuple

from bson import ObjectId

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
            obj_id = ObjectId(song_id)
        except Exception:
            raise ValueError(f"Invalid song_id: {song_id}") from None

        rating = Rating(song_id=song_id, rating=rating_value)
        rating.save()
        return rating

    def get_rating_stats(self, song_id: str) -> Tuple[float, int, int]:
        """
        Compute average, minimum, and maximum rating for a given song.

        Raises:
          ValueError: if `song_id` is invalid.

        Returns:
          (average: float, lowest: int, highest: int)
        """
        try:
            ObjectId(song_id)
        except Exception:
            raise ValueError(f"Invalid song_id: {song_id}") from None

        pipeline: List[Dict[str, Any]] = [
            {"$match": {"song_id": song_id}},
            {
                "$group": {
                    "_id": None,
                    "avg": {"$avg": "$rating"},
                    "min": {"$min": "$rating"},
                    "max": {"$max": "$rating"},
                },
            },
        ]
        result = Rating.objects.aggregate(*pipeline)

        try:
            stats = next(result)
            return stats.get("avg", 0.0), stats.get("min", 0), stats.get("max", 0)
        except StopIteration:
            return 0.0, 0, 0
