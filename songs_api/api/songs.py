from flask import Blueprint
from flask_pydantic import validate

from songs_api.schemas.api.song import (
    AverageDifficultyResponse,
    DifficultyParams,
    ListSongsParams,
    PagedSongsResponse,
    SearchSongsParams,
    SongResponse,
)
from songs_api.services.song_service import song_service

songs_bp = Blueprint("songs", __name__, url_prefix="/songs")


@songs_bp.route("", methods=["GET"])
@validate(query=ListSongsParams)
async def get_songs(params: ListSongsParams) -> PagedSongsResponse:
    """A: List songs with pagination."""
    page_obj = await song_service.list_songs(page=params.page, size=params.size)
    items = [SongResponse.model_validate(item.model_dump()) for item in page_obj.items]

    return PagedSongsResponse(
        items=items,
        total=page_obj.total,
        page=page_obj.page,
        size=page_obj.size,
    )


@songs_bp.route("/difficulty", methods=["GET"])
@validate(query=DifficultyParams)
async def get_average_difficulty(params: DifficultyParams) -> AverageDifficultyResponse:
    """B: Get average difficulty, optionally filtered by level."""
    avg = await song_service.average_difficulty(level=params.level)
    return AverageDifficultyResponse(
        average_difficulty=avg,
    )


@songs_bp.route("/search", methods=["GET"])
@validate(query=SearchSongsParams)
async def search_songs(params: SearchSongsParams) -> list[SongResponse]:
    """C: Full-text search on artist/title."""
    items = await song_service.search_songs(params.message)
    return [SongResponse(**item.model_dump()) for item in items]
