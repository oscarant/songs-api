import pytest

from songs_api.db.repositories.rating_repository import RatingRepository


def test_add_rating(create_song) -> None:
    """Test adding a new rating."""
    # Arrange
    repo = RatingRepository()
    song_id = str(create_song.id)
    rating_value = 4

    # Act
    result = repo.add_rating(song_id, rating_value)

    # Assert
    assert result is not None
    assert result.song_id == song_id
    assert result.rating == rating_value


def test_add_rating_invalid_song_id() -> None:
    """Test adding a rating with an invalid song ID."""
    # Arrange
    repo = RatingRepository()
    invalid_id = "not-a-valid-id"

    # Act & Assert
    with pytest.raises(ValueError, match=f"Invalid song_id: {invalid_id}"):
        repo.add_rating(invalid_id, 5)


def test_get_rating_stats(create_song, create_ratings) -> None:
    """Test getting rating statistics."""
    # Arrange
    repo = RatingRepository()
    song_id = str(create_song.id)

    # Act
    avg, lowest, highest = repo.get_rating_stats(song_id)

    # Assert
    assert avg == 3.0  # Average of 1,2,3,4,5
    assert lowest == 1
    assert highest == 5


def test_get_rating_stats_no_ratings(create_song) -> None:
    """Test getting stats when no ratings exist."""
    # Arrange
    repo = RatingRepository()
    song_id = str(create_song.id)

    # Act
    avg, lowest, highest = repo.get_rating_stats(song_id)

    # Assert
    assert avg == 0.0
    assert lowest == 0
    assert highest == 0


def test_get_rating_stats_invalid_song_id() -> None:
    """Test getting stats with an invalid song ID."""
    # Arrange
    repo = RatingRepository()
    invalid_id = "not-a-valid-id"

    # Act & Assert
    with pytest.raises(ValueError, match=f"Invalid song_id: {invalid_id}"):
        repo.get_rating_stats(invalid_id)
