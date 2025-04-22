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

| Route | Description
|
|
-------
|
-------------
|
|
`GET /songs`
|
List songs with pagination
|
|
`GET /songs/difficulty`
|
Get average difficulty, optionally filtered by level
|
|
`GET /songs/search`
|
Search songs by artist or title
|
|
`POST /ratings`
|
Add a rating for a song
|
|
`GET /ratings/<song_id>/stats`
|
Get rating statistics for a song
|

## Getting Started

### Prerequisites

- Python 3.9+
- MongoDB 4.4+ (or Docker)
- Poetry (for Python dependency management)

### Setup with Docker

The easiest way to run the application is with Docker Compose:

```bash
# Clone the repository
git clone
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
### Run Tests
To run the tests, you can use the following command:

```bash
docker-compose run --rm api pytest
```
This will run all the tests in the `tests` directory.
