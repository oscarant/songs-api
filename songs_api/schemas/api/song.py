from datetime import date
from typing import List, Optional

from pydantic import BaseModel, Field, field_serializer


# --- Response Schemas ---
class SongResponse(BaseModel):
    id: str
    artist: str
    title: str
    difficulty: float
    level: int
    released: date

    @field_serializer("released")
    def serialize_released(self, dt: date) -> str:
        """Convert date to string format YYYY-MM-DD."""
        return dt.strftime("%Y-%m-%d")


class SongListResponse(BaseModel):
    songs: List[SongResponse]


class PagedSongsResponse(BaseModel):
    items: List[SongResponse]
    total: int
    page: int
    size: int


class AverageDifficultyResponse(BaseModel):
    average_difficulty: float


# --- Query/Request Schemas ---
class ListSongsParams(BaseModel):
    page: int = Field(1, ge=1, description="Page number (1-based)")
    size: Optional[int] = Field(None, ge=1, description="Items per page")


class DifficultyParams(BaseModel):
    level: Optional[int] = Field(None, ge=1, description="Filter by song level")


class SearchSongsParams(BaseModel):
    message: str = Field(..., min_length=1, description="Search text for artist/title")
