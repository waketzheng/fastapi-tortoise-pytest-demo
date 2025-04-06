from __future__ import annotations

import os
import sys

import pytest
from asynctor import AsyncClientGenerator, AsyncTestClient

# Must set env before importing main.app
os.environ["DB_URL"] = "sqlite://:memory:"
try:
    from main import app
except ImportError:
    import sys
    from pathlib import Path

    sys.path.append(str(Path(__file__).parent.parent))
    from main import app


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session")
async def client() -> AsyncClientGenerator:
    async with AsyncTestClient(app) as c:
        yield c
