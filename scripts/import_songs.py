"""Script to import songs.json data into MongoDB."""

import asyncio
import json
from datetime import datetime
from pathlib import Path

import motor.motor_asyncio
from beanie import init_beanie

from songs_api.config import Settings
from songs_api.db.models.song import Song


def import_songs(file_path: str, drop_existing: bool = False) -> None:
    """Import songs from JSON file to MongoDB."""
    print(f"Importing songs from {file_path}...")

    # Initialize MongoDB connection and Beanie
    settings = Settings()
    client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGO_URI)
    db = client.get_default_database()

    # Run async init in a synchronous context
    loop = asyncio.new_event_loop()
    try:
        loop.run_until_complete(init_beanie(database=db, document_models=[Song]))
    finally:
        loop.close()

    # Drop existing collection if requested
    if drop_existing:
        print("Dropping existing songs collection...")
        loop = asyncio.new_event_loop()
        try:
            loop.run_until_complete(db.drop_collection("songs"))
        finally:
            loop.close()

    # Read and parse songs data
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(path, "r", encoding="utf-8") as f:
        # The file contains one JSON object per line
        songs_data = [json.loads(line) for line in f if line.strip()]

    songs = []
    for song_data in songs_data:
        # Convert released string to date object
        released_date = datetime.strptime(song_data["released"], "%Y-%m-%d").date()

        songs.append(
            Song(
                artist=song_data["artist"],
                title=song_data["title"],
                difficulty=song_data["difficulty"],
                level=song_data["level"],
                released=released_date,
            )
        )

    # Insert all songs at once
    print(f"Inserting {len(songs)} songs...")
    loop = asyncio.new_event_loop()
    try:
        result = loop.run_until_complete(Song.insert_many(songs))
        print(f"Successfully imported {len(result.inserted_ids)} songs")
    finally:
        loop.close()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Import songs data into MongoDB")
    parser.add_argument(
        "--file",
        default="songs.json",
        help="Path to songs.json file (default: songs.json)",
    )
    parser.add_argument(
        "--drop",
        action="store_true",
        help="Drop existing songs collection before import",
    )

    args = parser.parse_args()

    import_songs(args.file, args.drop)
