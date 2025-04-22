import logging
from typing import Optional

from flask import Flask

from songs_api.api.health import health_bp
from songs_api.config import Settings, settings
from songs_api.db.client import connect_db
from songs_api.exceptions.handlers import register_error_handlers


def create_app(config: Optional[Settings] = None) -> Flask:
    """
    Create and configure the Flask application.

    Args:
        config: Optional Settings instance to configure the app

    Returns:
        Flask app instance.
    """
    app_config = config or settings
    app = Flask(__name__)

    # Configure Flask app
    app.config["TESTING"] = app_config.TESTING
    app.config["DEBUG"] = app_config.DEBUG

    # Configure logging
    if not app.debug:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )

    # Connect to MongoDB
    connect_db()

    # Register Flask blueprints
    from songs_api.api.ratings import ratings_bp
    from songs_api.api.songs import songs_bp

    app.register_blueprint(songs_bp)
    app.register_blueprint(ratings_bp)
    app.register_blueprint(health_bp)

    # Register error handlers
    register_error_handlers(app)

    return app
