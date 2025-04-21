"""Test configuration for pytest."""

import asyncio
import os
from unittest.mock import AsyncMock, patch

import pytest

# Set test environment variables
os.environ["MONGO_URI"] = "mongodb://localhost:27017/songs_test"


@pytest.fixture(scope="session")
def event_loop():
    """Create an event loop for the test session."""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(autouse=True)
async def mock_beanie_init():
    """Mock beanie initialization to avoid connecting to a real database."""
    with patch("songs_api.main.init_beanie") as mock:
        mock.return_value = AsyncMock()
        yield mock


@pytest.fixture(autouse=True)
async def mock_motor_client():
    """Mock MongoDB client to avoid connecting to a real database."""
    with patch("songs_api.db.client.AsyncIOMotorClient") as mock:
        client_instance = AsyncMock()
        mock.return_value = client_instance
        db_instance = AsyncMock()
        client_instance.get_default_database.return_value = db_instance
        yield mock
