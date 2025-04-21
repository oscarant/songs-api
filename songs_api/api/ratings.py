from flask import Blueprint
from flask_pydantic import validate

from songs_api.schemas.api.rating import (
    RatingCreateRequest,
    RatingResponse,
    RatingStatsResponse,
)
from songs_api.services.rating_service import rating_service

ratings_bp = Blueprint("ratings", __name__)


@ratings_bp.route("/ratings", methods=["POST"])
@validate(body=RatingCreateRequest)
def create_rating(body: RatingCreateRequest) -> RatingResponse:
    """D: Add a new rating for a song."""
    entity = rating_service.add_rating(
        song_id=body.song_id,
        rating_value=body.rating,
    )
    return RatingResponse.model_validate(entity.model_dump())


@ratings_bp.route("/ratings/<song_id>/stats", methods=["GET"])
@validate()
def get_rating_stats(song_id: str) -> RatingStatsResponse:
    """E: Retrieve average, lowest, and highest rating for a song."""
    stats = rating_service.get_stats(song_id)
    return RatingStatsResponse.model_validate(stats.model_dump())
