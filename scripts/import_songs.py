"""Script to import songs.json data into MongoDB."""

import json
from datetime import datetime
from pathlib import Path

from mongoengine import connect, disconnect

from songs_api.config import Settings
from songs_api.db.models.song import Song


def import_songs(file_path: str, drop_existing: bool = False) -> None:
    """Import songs from JSON file to MongoDB."""
    print(f"Importing songs from {file_path}...")

    # Initialize MongoDB connection
    settings = Settings()
    connect(host=settings.MONGO_URI)

    # Drop existing collection if requested
    if drop_existing:
        print("Dropping existing songs collection...")
        Song.drop_collection()

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

        song = Song(
            artist=song_data["artist"],
            title=song_data["title"],
            difficulty=song_data["difficulty"],
            level=song_data["level"],
            released=released_date,
        )
        songs.append(song)

    # Insert songs
    print(f"Inserting {len(songs)} songs...")
    for song in songs:
        song.save()

    print(f"Successfully imported {len(songs)} songs")
    disconnect()


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
