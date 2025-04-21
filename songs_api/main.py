from flask import Flask

from songs_api.config import Settings
from songs_api.db.client import get_client
from songs_api.db.init_db import init_db
from songs_api.exceptions.handlers import register_error_handlers


def create_app() -> Flask:
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
    db_client = get_client()

    # Initialize Beanie synchronously
    init_db(db_client, [Song, Rating])

    # Register Flask blueprints
    from songs_api.api.ratings import ratings_bp
    from songs_api.api.songs import songs_bp

    app.register_blueprint(songs_bp)
    app.register_blueprint(ratings_bp)

    # Register error handlers
    register_error_handlers(app)

    return app
