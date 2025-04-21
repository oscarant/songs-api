from typing import ClassVar

from mongoengine import Document, IntField, StringField


class Rating(Document):
    """Rating document model."""

    song_id = StringField(required=True)
    rating = IntField(required=True, min_value=1, max_value=5)

    meta: ClassVar = {
        "collection": "ratings",
        "indexes": ["song_id", {"fields": ["song_id", "rating"]}],
    }
