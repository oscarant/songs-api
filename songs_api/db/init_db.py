import asyncio
from typing import Any, List, Type

from beanie import Document, init_beanie
from motor.motor_asyncio import AsyncIOMotorClient


def init_db(
    client: AsyncIOMotorClient[Any],
    document_models: List[Type[Document]],
) -> None:
    """Initialize Beanie by running the async init in a synchronous context."""

    async def _init() -> None:
        await init_beanie(
            database=client.get_default_database(),
            document_models=document_models,
        )

    # Create a new event loop for this function
    loop = asyncio.new_event_loop()
    try:
        loop.run_until_complete(_init())
    finally:
        loop.close()
