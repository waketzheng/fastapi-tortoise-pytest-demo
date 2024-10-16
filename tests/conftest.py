import os
from typing import AsyncGenerator, Optional

import pytest
from asgi_lifespan import LifespanManager
from httpx import ASGITransport, AsyncClient
from typing_extensions import Self

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


class TestClient(AsyncClient):
    def __init__(self, app, base_url="http://test", mount_lifespan=True, **kw) -> None:
        self.mount_lifespan = mount_lifespan
        self._manager: Optional[LifespanManager] = None
        super().__init__(transport=ASGITransport(app), base_url=base_url, **kw)

    async def __aenter__(self) -> Self:
        if self.mount_lifespan:
            app = self._transport.app  # type:ignore
            self._manager = await LifespanManager(app).__aenter__()
            self._transport = ASGITransport(app=self._manager.app)
        return await super().__aenter__()

    async def __aexit__(self, *args, **kw):
        await super().__aexit__(*args, **kw)
        if self._manager is not None:
            await self._manager.__aexit__(*args, **kw)


@pytest.fixture(scope="session")
async def client() -> AsyncGenerator[TestClient, None]:
    async with TestClient(app) as c:
        yield c
