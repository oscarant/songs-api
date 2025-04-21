from datetime import date
from typing import ClassVar

from beanie import Document, Indexed
from pydantic import Field


class Song(Document):
    """Beanie Document for a song entry."""

    artist: str = Indexed()
    title: str = Indexed()
    difficulty: float = Field(ge=0)
    level: int = Indexed(ge=1)
    released: date

    class Settings:
        name: ClassVar[str] = "songs"
        indexes: ClassVar[list] = [  # type: ignore[type-arg]
            [("artist", "text"), ("title", "text")],  # full-text search
            [("level", 1)],  # filter by level
        ]
