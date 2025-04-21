from pydantic import BaseModel


class RatingEntity(BaseModel):
    id: str
    song_id: str
    rating: int

    model_config = {"from_attributes": True}


class RatingStatsEntity(BaseModel):
    average: float
    lowest: int
    highest: int

    model_config = {"from_attributes": True}
