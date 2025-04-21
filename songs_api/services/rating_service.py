from dataclasses import dataclass, field

from songs_api.db.repositories.rating_repository import RatingRepository, rating_repo
from songs_api.exceptions.custom import NotFoundError
from songs_api.schemas.entities.rating import RatingEntity, RatingStatsEntity


@dataclass
class RatingService:
    """Orchestrates rating operations and maps results to domain entities."""

    repo: RatingRepository = field(default_factory=lambda: rating_repo)

    async def add_rating(self, song_id: str, rating_value: int) -> RatingEntity:
        """Add a new rating; raise NotFoundError on invalid song."""
        try:
            rating_doc = await self.repo.add_rating(
                song_id=song_id,
                rating_value=rating_value,
            )
        except ValueError as e:
            raise NotFoundError(str(e)) from e

        # Map to domain entity
        return RatingEntity(
            id=str(rating_doc.id),
            song_id=str(rating_doc.song_id),
            rating=rating_doc.rating,
        )

    async def get_stats(self, song_id: str) -> RatingStatsEntity:
        """Fetch rating stats; raise NotFoundError on invalid song."""
        try:
            avg, lowest, highest = await self.repo.get_rating_stats(song_id)
        except ValueError as e:
            raise NotFoundError(str(e)) from e

        # Map to domain entity for stats
        return RatingStatsEntity(
            average=avg,
            lowest=lowest,
            highest=highest,
        )


# Module-level singleton
rating_service = RatingService()
