import pytest

from songs_api.db.repositories.song_repository import SongRepository


def test_list_songs_empty() -> None:
    """Test listing songs when DB is empty."""
    # Arrange
    repo = SongRepository()

    # Act
    songs, total = repo.list_songs()

    # Assert
    assert len(songs) == 0
    assert total == 0


def test_list_songs(create_songs) -> None:
    """Test listing songs with pagination."""
    # Arrange
    repo = SongRepository()

    # Act - first page with default size
    songs, total = repo.list_songs(page=1)

    # Assert
    assert len(songs) == len(create_songs)
    assert total == len(create_songs)

    # Act - with custom size
    songs, total = repo.list_songs(page=1, size=1)

    # Assert
    assert len(songs) == 1
    assert total == len(create_songs)

    # Act - second page
    songs, total = repo.list_songs(page=2, size=1)

    # Assert
    assert len(songs) == 1
    assert total == len(create_songs)


def test_average_difficulty(create_songs) -> None:
    """Test calculating average difficulty."""
    # Arrange
    repo = SongRepository()

    # Act
    avg = repo.average_difficulty()

    # Assert - average of 5.0, 10.0, 7.5
    assert avg == 7.5


def test_average_difficulty_filtered_by_level(create_songs) -> None:
    """Test average difficulty filtered by level."""
    # Arrange
    repo = SongRepository()
    level = 10

    # Act
    avg = repo.average_difficulty(level=level)

    # Assert - only one song with level 10 has difficulty 10.0
    assert avg == 10.0


def test_average_difficulty_empty() -> None:
    """Test average difficulty when no songs exist."""
    # Arrange
    repo = SongRepository()

    # Act
    avg = repo.average_difficulty()

    # Assert
    assert avg == 0.0


def test_search_songs(create_songs) -> None:
    """Test searching for songs."""
    # Arrange
    repo = SongRepository()

    # Act - search by artist
    songs = repo.search_songs("One")

    # Assert
    assert len(songs) == 1
    assert songs[0].artist == "Artist One"

    # Act - search by title
    songs = repo.search_songs("Second")

    # Assert
    assert len(songs) == 1
    assert songs[0].title == "Second Song"

    # Act - search with no matches
    songs = repo.search_songs("Nonexistent")

    # Assert
    assert len(songs) == 0


def test_get_song_by_id(create_song) -> None:
    """Test getting a song by ID."""
    # Arrange
    repo = SongRepository()
    song_id = str(create_song.id)

    # Act
    song = repo.get_song_by_id(song_id)

    # Assert
    assert song is not None
    assert str(song.id) == song_id
    assert song.artist == create_song.artist


def test_get_song_by_id_invalid() -> None:
    """Test getting a song with an invalid ID."""
    # Arrange
    repo = SongRepository()
    invalid_id = "not-a-valid-id"

    # Act & Assert
    with pytest.raises(ValueError, match=f"Invalid song_id: {invalid_id}"):
        repo.get_song_by_id(invalid_id)
