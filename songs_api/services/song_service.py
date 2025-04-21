from dataclasses import dataclass, field
from typing import List, Optional

from songs_api.db.repositories.song_repository import SongRepository
from songs_api.exceptions.custom import NotFoundError
from songs_api.schemas.entities.song import SongEntity
from songs_api.utils.pagination import Page


@dataclass
class SongService:
    """Orchestrates song-related operations, mapping repo calls to domain entities."""

    repo: SongRepository = field(default_factory=SongRepository)

    def list_songs(
        self,
        page: int = 1,
        size: Optional[int] = None,
    ) -> Page[SongEntity]:
        """Return a paginated list of SongEntity."""
        items, total = self.repo.list_songs(page=page, size=size)

        entities: List[SongEntity] = []
        for doc in items:
            data = doc.model_dump()
            data["id"] = str(doc.id)
            entities.append(SongEntity.model_validate(data))

        return Page[SongEntity](
            items=entities,
            total=total,
            page=page,
            size=len(entities),
        )

    def average_difficulty(self, level: Optional[int] = None) -> float:
        """Get average difficulty, optionally filtering by level."""
        return self.repo.average_difficulty(level)

    async def search_songs(self, message: str) -> List[SongEntity]:
        """Search songs by text, returning domain entities."""
        docs = self.repo.search_songs(message)
        return [
            SongEntity.model_validate({**doc.model_dump(), "id": str(doc.id)})
            for doc in docs
        ]

    def get_song(self, song_id: str) -> SongEntity:
        """Fetch a single song entity or raise NotFoundError."""
        try:
            doc = self.repo.get_song_by_id(song_id)
        except ValueError as e:
            raise NotFoundError(str(e)) from e
        data = doc.model_dump()
        data["id"] = str(doc.id)
        return SongEntity.model_validate(data)


# Module-level singleton for convenience
song_service = SongService()
