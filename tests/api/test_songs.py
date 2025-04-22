import json


def test_get_songs(client, create_songs) -> None:
    """Test GET /songs endpoint."""
    # Act
    response = client.get("/songs")
    data = json.loads(response.data)

    # Assert
    assert response.status_code == 200
    assert "items" in data
    assert "total" in data
    assert "page" in data
    assert "size" in data
    assert len(data["items"]) == len(create_songs)
    assert data["total"] == len(create_songs)
    assert data["page"] == 1


def test_get_songs_pagination(client, create_songs) -> None:
    """Test GET /songs with pagination parameters."""
    # Act
    response = client.get("/songs?page=2&size=1")
    data = json.loads(response.data)

    # Assert
    assert response.status_code == 200
    assert len(data["items"]) == 1
    assert data["page"] == 2
    assert data["size"] == 1


def test_get_average_difficulty(client, create_songs) -> None:
    """Test GET /songs/difficulty endpoint."""
    # Act
    response = client.get("/songs/difficulty")
    data = json.loads(response.data)

    # Assert
    assert response.status_code == 200
    assert "average_difficulty" in data
    # Average of 5.0, 10.0, 7.5
    assert data["average_difficulty"] == 7.5


def test_get_average_difficulty_filtered(client, create_songs) -> None:
    """Test GET /songs/difficulty with level filter."""
    # Act
    response = client.get("/songs/difficulty?level=10")
    data = json.loads(response.data)

    # Assert
    assert response.status_code == 200
    assert data["average_difficulty"] == 10.0


def test_search_songs(client, create_songs) -> None:
    """Test GET /songs/search endpoint."""
    # Act
    response = client.get("/songs/search?message=One")
    data = json.loads(response.data)

    # Assert
    assert response.status_code == 200
    assert "songs" in data
    assert len(data["songs"]) == 1
    assert data["songs"][0]["artist"] == "Artist One"


def test_search_songs_no_results(client, create_songs) -> None:
    """Test search with no matching results."""
    # Act
    response = client.get("/songs/search?message=NonexistentArtist")
    data = json.loads(response.data)

    # Assert
    assert response.status_code == 200
    assert "songs" in data
    assert len(data["songs"]) == 0


def test_search_songs_missing_message(client) -> None:
    """Test search without required message parameter."""
    # Act
    response = client.get("/songs/search")
    data = json.loads(response.data)

    # Assert
    assert response.status_code == 400
    assert "validation_error" in data
