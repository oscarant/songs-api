# Songs API

A Flask-based RESTful API for managing songs and their ratings, using MongoDB as a data store.

## Features

- **Song Listing**: Paginated list of songs with filtering options
- **Difficulty Analysis**: Calculate average song difficulty, with optional level filtering
- **Search Functionality**: Full-text search on song title and artist
- **Rating System**: Add ratings for songs and retrieve rating statistics
- **MongoDB Integration**: Efficient data storage with proper indexing
- **Scalable Architecture**: Designed to handle millions of songs and ratings

## Tech Stack

- **Python 3.13**: Modern Python features
- **Flask**: Lightweight web framework
- **MongoDB**: NoSQL database
- **MongoEngine**: MongoDB ODM (Object Document Mapper)
- **Pydantic**: Data validation and settings management
- **Poetry**: Dependency management
- **Docker & Docker Compose**: Containerization

## API Endpoints

| Route | Method | Description | Parameters | Response |
|-------|--------|-------------|------------|----------|
| `/songs` | GET | List songs with pagination | `page`: Page number (1-based)<br>`size`: Items per page | List of songs with pagination details |
| `/songs/difficulty` | GET | Get average difficulty | `level`: (Optional) Filter by song level | Average difficulty value |
| `/songs/search` | GET | Search songs by artist or title | `message`: Search text for artist/title | List of matching songs |
| `/ratings` | POST | Add a rating for a song | Body: `song_id`: ID of song<br>`rating`: Value from 1-5 | Created rating details |
| `/ratings/<song_id>/stats` | GET | Get rating statistics for a song | `song_id`: in path | Average, lowest and highest ratings |
| `/health` | GET | Service health check | None | Service and database status |

## Getting Started

### Prerequisites

- Python 3.9+
- MongoDB 4.4+ (or Docker)
- Poetry (for Python dependency management)

### Setup with Docker

The easiest way to run the application is with Docker Compose:

```bash
cd songs-api

# Start the application with Docker Compose
docker-compose up -d
```

This will:
1) Start a MongoDB instance
2) Build and start the Songs API
3) Import sample data automatically

The API will be available at http://localhost:5000

## Testing

### Docker
To run the tests in Docker, you can use the following command:

```bash
docker-compose run --build --rm songs_api pytest -vv .
```

### Local + Docker
For running tests on your local machine.
1. You need to start a database (or have the docker-compose running).

if you don't have the docker-compose running, you can start a mongodb
instance with docker using this command:
```bash
docker run --detach --name songs_db --publish 127.0.0.1:27017:27017 mongo:4.4
```

2. You need to make the local environment setup with poetry:

```bash
poetry install
```

Then you can run the tests with:

```bash
pytest -vv .
```


This will run all the tests in the `tests` directory.

`
