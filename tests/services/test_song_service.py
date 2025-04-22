from datetime import date
from unittest.mock import MagicMock

import pytest

from songs_api.db.repositories.song_repository import SongRepository
from songs_api.exceptions.custom import NotFoundError
from songs_api.services.song_service import SongService


@pytest.fixture
def mock_repo():
    """Create a mock song repository."""
    return MagicMock(spec=SongRepository)


@pytest.fixture
def service(mock_repo):
    """Create a song service with a mock repository."""
    return SongService(repo=mock_repo)


def test_list_songs(service, mock_repo) -> None:
    """Test listing songs."""
    # Arrange
    page = 1
    size = 10

    # Create mock songs
    mock_songs = [MagicMock() for _ in range(3)]
    for i, song in enumerate(mock_songs):
        song.id = f"id{i}"
        song.artist = f"Artist {i}"
        song.title = f"Song {i}"
        song.difficulty = float(i + 5)
        song.level = i + 5
        song.released = date.today()

    mock_repo.list_songs.return_value = (mock_songs, len(mock_songs))

    # Act
    result = service.list_songs(page=page, size=size)

    # Assert
    mock_repo.list_songs.assert_called_once_with(page=page, size=size)
    assert len(result.items) == len(mock_songs)
    assert result.total == len(mock_songs)
    assert result.page == page
    assert result.size == len(mock_songs)


def test_average_difficulty(service, mock_repo) -> None:
    """Test getting average difficulty."""
    # Arrange
    level = 5
    expected_avg = 7.5
    mock_repo.average_difficulty.return_value = expected_avg

    # Act
    result = service.average_difficulty(level=level)

    # Assert
    mock_repo.average_difficulty.assert_called_once_with(level=level)
    assert result == expected_avg


def test_search_songs(service, mock_repo) -> None:
    """Test searching songs."""
    # Arrange
    search_text = "test query"

    # Create mock songs
    mock_songs = [MagicMock() for _ in range(2)]
    for i, song in enumerate(mock_songs):
        song.id = f"id{i}"
        song.artist = f"Artist {i}"
        song.title = f"Song {i}"
        song.difficulty = float(i + 5)
        song.level = i + 5
        song.released = date.today()

    mock_repo.search_songs.return_value = mock_songs

    # Act
    result = service.search_songs(search_text)

    # Assert
    mock_repo.search_songs.assert_called_once_with(search_text)
    assert len(result) == len(mock_songs)


def test_get_song_success(service, mock_repo, valid_object_id) -> None:
    """Test getting a single song."""
    # Arrange
    song_id = valid_object_id

    mock_song = MagicMock()
    mock_song.id = song_id
    mock_song.artist = "Test Artist"
    mock_song.title = "Test Song"
    mock_song.difficulty = 8.5
    mock_song.level = 8
    mock_song.released = date.today()

    mock_repo.get_song_by_id.return_value = mock_song

    # Act
    result = service.get_song(song_id)

    # Assert
    mock_repo.get_song_by_id.assert_called_once_with(song_id)
    assert result.id == song_id
    assert result.artist == mock_song.artist
    assert result.title == mock_song.title


def test_get_song_not_found(service, mock_repo) -> None:
    """Test getting a song that doesn't exist."""
    # Arrange
    invalid_id = "invalid-id"
    error_msg = f"Invalid song_id: {invalid_id}"
    mock_repo.get_song_by_id.side_effect = ValueError(error_msg)

    # Act & Assert
    with pytest.raises(NotFoundError, match=error_msg):
        service.get_song(invalid_id)
