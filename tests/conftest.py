from __future__ import annotations

import os

from asynctor.testing import anyio_backend_fixture, async_client_fixture
from asynctor.utils import ExtendSyspath

# Must set env before importing main.app
os.environ["DB_URL"] = "sqlite://:memory:"
with ExtendSyspath(".."):
    from app.main import app


anyio_backend = anyio_backend_fixture()
client = async_client_fixture(app)
