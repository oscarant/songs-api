from pydantic import BaseModel


class RatingEntity(BaseModel):
    id: str
    song_id: str
    rating: int

    model_config = {"from_attributes": True}
