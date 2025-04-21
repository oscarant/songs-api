from typing import Any

from beanie import init_beanie
from flask import Flask
from motor.motor_asyncio import AsyncIOMotorClient

from songs_api.config import Settings
from songs_api.db.client import get_client
from songs_api.exceptions.handlers import register_error_handlers


async def create_app() -> Flask:
    """
    Create and configure the Flask application.
    :return: Flask app instance.
    """
    Settings()
    app = Flask(__name__)

    # Import Beanie document models here to avoid circular imports
    from songs_api.db.models.rating import Rating
    from songs_api.db.models.song import Song

    # Initialize Mongo client (cached) and Beanie
    db_client: AsyncIOMotorClient[Any] = get_client()
    await init_beanie(
        database=db_client.get_default_database(),
        document_models=[Song, Rating],
    )

    # Register Flask blueprints
    from songs_api.api.ratings import ratings_bp
    from songs_api.api.songs import songs_bp

    app.register_blueprint(songs_bp)
    app.register_blueprint(ratings_bp)

    # Register error handlers
    register_error_handlers(app)

    return app
