from mongoengine import Document, ReferenceField, IntField, StringField
from songs_api.db.models.song import Song

class Rating(Document):
    """Rating document model."""

    song_id = StringField(required=True)
    rating = IntField(required=True, min_value=1, max_value=5)

    meta = {
        'collection': 'ratings',
        'indexes': [
            'song_id',
            {
                'fields': ['song_id', 'rating']
            }
        ]
    }
