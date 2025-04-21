from typing import ClassVar

from mongoengine import DateField, Document, FloatField, IntField, StringField


class Song(Document):
    """MongoEngine Document for a song entry."""

    artist = StringField(required=True)
    title = StringField(required=True)
    difficulty = FloatField(min_value=0, required=True)
    level = IntField(min_value=1, required=True)
    released = DateField(required=True)

    meta: ClassVar = {
        "collection": "songs",
        "indexes": [
            {
                "fields": ["$artist", "$title"],
                "default_language": "english",
            },  # full-text search
            {"fields": ["level"]},  # filter by level
        ],
    }
