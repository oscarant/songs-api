from datetime import date

from pydantic import BaseModel


class SongEntity(BaseModel):
    id: str
    artist: str
    title: str
    difficulty: float
    level: int
    released: date

    model_config = {
        "from_attributes": True,  # allow instantiation from ORM/document objects
    }
