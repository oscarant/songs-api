from datetime import date, timedelta
from typing import Dict, List

import mongoengine
import pytest
from bson import ObjectId
from mongoengine import connect, disconnect

from songs_api.config import Settings
from songs_api.db.models.rating import Rating
from songs_api.db.models.song import Song
from songs_api.main import create_app


@pytest.fixture(scope="session")
def test_settings():
    """Create test settings."""
    return Settings.get_test_settings()


@pytest.fixture(scope="session")
def app(test_settings):
    """Create and configure a Flask app for testing."""
    # Create the Flask app with test settings
    app = create_app(config=test_settings)

    # Return the app for testing
    yield app


@pytest.fixture(scope="session")
def client(app):
    """Create a test client for the app."""
    with app.test_client() as client:
        yield client


@pytest.fixture(scope="function", autouse=True)
def db(test_settings):
    """Set up and tear down the database for each test."""
    # Disconnect any existing test connections first
    disconnect(alias="testdb")

    # Connect to the test database with a test-specific alias
    connect(host=test_settings.MONGO_URI, alias="testdb")

    # Set the test db as default for the models
    mongoengine.context_managers.switch_db(Song, "testdb")
    mongoengine.context_managers.switch_db(Rating, "testdb")

    # Clear any existing data
    Song.drop_collection()
    Rating.drop_collection()

    # Create test data
    yield

    # Clean up after the test
    disconnect(alias="testdb")


@pytest.fixture
def song_data() -> Dict:
    """Return sample song data."""
    return {
        "artist": "Test Artist",
        "title": "Test Song",
        "difficulty": 10.5,
        "level": 8,
        "released": date.today() - timedelta(days=30),
    }


@pytest.fixture
def songs_data() -> List[Dict]:
    """Return a list of sample songs."""
    return [
        {
            "artist": "Artist One",
            "title": "First Song",
            "difficulty": 5.0,
            "level": 5,
            "released": date.today() - timedelta(days=100),
        },
        {
            "artist": "Artist Two",
            "title": "Second Song",
            "difficulty": 10.0,
            "level": 10,
            "released": date.today() - timedelta(days=50),
        },
        {
            "artist": "Artist Three",
            "title": "Third Song",
            "difficulty": 7.5,
            "level": 7,
            "released": date.today() - timedelta(days=25),
        },
    ]


@pytest.fixture
def create_song(song_data) -> Song:
    """Create and return a test song."""
    song = Song(**song_data)
    song.save()
    return song


@pytest.fixture
def create_songs(songs_data) -> List[Song]:
    """Create and return multiple test songs."""
    songs = []
    for data in songs_data:
        song = Song(**data)
        song.save()
        songs.append(song)
    return songs


@pytest.fixture
def create_ratings(create_song) -> List[Rating]:
    """Create test ratings for a song."""
    ratings = []
    for i in range(1, 6):
        rating = Rating(song_id=str(create_song.id), rating=i)
        rating.save()
        ratings.append(rating)
    return ratings


@pytest.fixture
def valid_object_id() -> str:
    """Return a valid ObjectId as string."""
    return str(ObjectId())
