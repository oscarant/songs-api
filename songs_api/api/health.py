from flask import Blueprint, Response, jsonify

from songs_api.db.client import get_db

health_bp = Blueprint("health", __name__)


# Add health check endpoint
@health_bp.route("/health", methods=["GET"])
def health_check() -> tuple[Response, int]:
    """Health check endpoint to verify the service and database status."""
    try:
        # Check MongoDB connection
        db = get_db()
        db.command("ping")
        return jsonify({"status": "healthy", "database": "connected"}), 200
    except Exception:
        return jsonify({"status": "unhealthy", "database": "disconnected"}), 503
