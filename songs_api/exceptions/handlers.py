from flask import Flask, Response, jsonify
from pydantic import ValidationError

from songs_api.exceptions.custom import NotFoundError


def register_error_handlers(app: Flask) -> None:
    """Attach global error handlers to the Flask app."""

    @app.errorhandler(ValidationError)
    def handle_validation(e: ValidationError) -> tuple[Response, int]:
        return jsonify({"error": "Validation Error", "messages": e.errors()}), 400

    @app.errorhandler(NotFoundError)
    def handle_not_found(e: NotFoundError) -> tuple[Response, int]:
        return jsonify({"error": "Not Found", "message": str(e)}), 404

    @app.errorhandler(Exception)
    def handle_generic(e: Exception) -> tuple[Response, int]:
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500
