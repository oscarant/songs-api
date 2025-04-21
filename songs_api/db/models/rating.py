from typing import ClassVar

from beanie import Document, Indexed, PydanticObjectId
from pydantic import Field


class Rating(Document):
    """Beanie Document for a song rating."""

    song_id: PydanticObjectId = Indexed()  # Reference to the Song document
    rating: int = Field(ge=1, le=5)  # Rating between 1 and 5 inclusive

    class Settings:
        name: ClassVar[str] = "ratings"
        indexes: ClassVar[list] = [  # type: ignore[type-arg]
            [("song_id", 1)],  # look up ratings by song
            [("song_id", 1), ("rating", 1)],  # optimize aggregated queries
        ]
