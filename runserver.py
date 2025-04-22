"""Entry point for running the Flask application."""

from songs_api.main import create_app
from songs_api.config import settings

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=settings.DEBUG)
