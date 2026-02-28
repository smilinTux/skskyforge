"""
SKSkyforge FastAPI web application.

Copyright (C) 2025 S&K Holding QT (Quantum Technologies)
SK = staycuriousANDkeepsmilin

This file is part of SKSkyforge.
Licensed under AGPL-3.0. See LICENSE for details.
"""

from fastapi import FastAPI

from .routers import router


def create_app() -> FastAPI:
    """Create and configure the SKSkyforge FastAPI application."""
    app = FastAPI(
        title="SKSkyforge",
        description="Sovereign Alignment Calendar API",
        version="1.1.0",
    )
    app.include_router(router, prefix="/api")
    return app
