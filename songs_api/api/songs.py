from flask import Blueprint
from flask_pydantic import validate

from songs_api.schemas.api.song import (
    AverageDifficultyResponse,
    DifficultyParams,
    ListSongsParams,
    PagedSongsResponse,
    SearchSongsParams,
    SongListResponse,
    SongResponse,
)
from songs_api.services.song_service import song_service

songs_bp = Blueprint("songs", __name__, url_prefix="/songs")


@songs_bp.route("", methods=["GET"])
@validate(query=ListSongsParams)
def get_songs(query: ListSongsParams) -> PagedSongsResponse:
    """A: List songs with pagination."""
    page_obj = song_service.list_songs(
        page=query.page,
        size=query.size,
    )
    items = [SongResponse.model_validate(item.model_dump()) for item in page_obj.items]

    return PagedSongsResponse(
        items=items,
        total=page_obj.total,
        page=page_obj.page,
        size=page_obj.size,
    )


@songs_bp.route("/difficulty", methods=["GET"])
@validate()
def get_average_difficulty(
    query: DifficultyParams,
) -> AverageDifficultyResponse:
    """B: Get average difficulty, optionally filtered by level."""
    avg = song_service.average_difficulty(level=query.level)
    return AverageDifficultyResponse(
        average_difficulty=avg,
    )


@songs_bp.route("/search", methods=["GET"])
@validate()
def search_songs(query: SearchSongsParams) -> SongListResponse:
    """C: Full-text search on artist/title."""
    items = song_service.search_songs(query.message)
    return SongListResponse(
        songs=[SongResponse.model_validate(item.model_dump()) for item in items],
    )
