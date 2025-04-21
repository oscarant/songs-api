from pydantic import BaseModel, Field


class RatingCreateRequest(BaseModel):
    song_id: str = Field(..., description="ID of the song to rate")
    rating: int = Field(..., ge=1, le=5, description="Rating between 1 and 5")


class RatingResponse(BaseModel):
    id: str
    song_id: str
    rating: int


class RatingStatsResponse(BaseModel):
    average: float = Field(..., description="Average rating of the song")
    lowest: int = Field(..., description="Lowest rating")
    highest: int = Field(..., description="Highest rating")
