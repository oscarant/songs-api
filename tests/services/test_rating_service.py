from unittest.mock import MagicMock

import pytest

from songs_api.db.repositories.rating_repository import RatingRepository
from songs_api.exceptions.custom import NotFoundError
from songs_api.services.rating_service import RatingService


@pytest.fixture
def mock_repo():
    """Create a mock rating repository."""
    return MagicMock(spec=RatingRepository)


@pytest.fixture
def service(mock_repo):
    """Create a rating service with a mock repository."""
    return RatingService(repo=mock_repo)


def test_add_rating_success(service, mock_repo, valid_object_id) -> None:
    """Test adding a rating successfully."""
    # Arrange
    song_id = valid_object_id
    rating_value = 4

    # Mock the repository response
    mock_rating = MagicMock()
    mock_rating.id = "rating_id"
    mock_rating.song_id = song_id
    mock_rating.rating = rating_value
    mock_repo.add_rating.return_value = mock_rating

    # Act
    result = service.add_rating(song_id, rating_value)

    # Assert
    mock_repo.add_rating.assert_called_once_with(
        song_id=song_id,
        rating_value=rating_value,
    )
    assert result.id == "rating_id"
    assert result.song_id == song_id
    assert result.rating == rating_value


def test_add_rating_not_found(service, mock_repo) -> None:
    """Test adding a rating with an invalid song ID."""
    # Arrange
    invalid_id = "invalid-id"
    mock_repo.add_rating.side_effect = ValueError(f"Invalid song_id: {invalid_id}")

    # Act & Assert
    with pytest.raises(NotFoundError, match=f"Invalid song_id: {invalid_id}"):
        service.add_rating(invalid_id, 5)


def test_get_stats_success(service, mock_repo, valid_object_id) -> None:
    """Test getting rating stats successfully."""
    # Arrange
    song_id = valid_object_id
    mock_repo.get_rating_stats.return_value = (4.5, 4, 5)

    # Act
    result = service.get_stats(song_id)

    # Assert
    mock_repo.get_rating_stats.assert_called_once_with(song_id)
    assert result.average == 4.5
    assert result.lowest == 4
    assert result.highest == 5


def test_get_stats_not_found(service, mock_repo) -> None:
    """Test getting stats with an invalid song ID."""
    # Arrange
    invalid_id = "invalid-id"
    mock_repo.get_rating_stats.side_effect = ValueError(
        f"Invalid song_id: {invalid_id}",
    )

    # Act & Assert
    with pytest.raises(NotFoundError, match=f"Invalid song_id: {invalid_id}"):
        service.get_stats(invalid_id)
