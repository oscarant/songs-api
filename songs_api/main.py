from flask import Flask

from songs_api.config import Settings
from songs_api.db.client import connect_db
from songs_api.exceptions.handlers import register_error_handlers


def create_app() -> Flask:
    """
    Create and configure the Flask application.
    :return: Flask app instance.
    """
    Settings()
    app = Flask(__name__)

    # Import Beanie document models here to avoid circular imports

    # Connect to MongoDB
    connect_db()

    # Register Flask blueprints
    from songs_api.api.ratings import ratings_bp
    from songs_api.api.songs import songs_bp

    app.register_blueprint(songs_bp)
    app.register_blueprint(ratings_bp)

    # Register error handlers
    register_error_handlers(app)

    # Set debug to true
    app.config["DEBUG"] = Settings().DEBUG

    return app
