"""Entry point for running the Flask application."""

import asyncio
from typing import Callable, TypeVar

from asgiref.wsgi import WsgiToAsgi
from hypercorn.asyncio import serve
from hypercorn.config import Config

from songs_api.main import create_app

T = TypeVar("T")


def run_async(coro: Callable[[], T]) -> T:
    """Run an async function in a new event loop."""
    return asyncio.run(coro())


async def main() -> None:
    """Start the application server."""
    print("Starting Songs API...")
    app = await create_app()

    # Convert the Flask app to ASGI
    asgi_app = WsgiToAsgi(app)

    # Configure Hypercorn
    config = Config()
    config.bind = ["0.0.0.0:5000"]
    config.use_reloader = True

    # Start the server
    await serve(asgi_app, config)


if __name__ == "__main__":
    asyncio.run(main())
