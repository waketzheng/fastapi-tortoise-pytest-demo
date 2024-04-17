from contextlib import asynccontextmanager

import pytest
from httpx import ASGITransport, AsyncClient
from tortoise import Tortoise

from main import app

DB_URL = "sqlite://:memory:"


async def init_db(db_url, create_db: bool = False, schemas: bool = False) -> None:
    """Initial database connection"""
    await Tortoise.init(
        db_url=db_url, modules={"models": ["models"]}, _create_db=create_db
    )
    if create_db:
        print(f"Database created! {db_url = }")
    if schemas:
        await Tortoise.generate_schemas()
        print("Success to generate schemas")


async def init(db_url: str = DB_URL) -> None:
    await init_db(db_url, True, True)


@asynccontextmanager
async def register_orm(drop=False):
    await init()
    yield
    if drop:
        await Tortoise._drop_databases()
    else:
        await Tortoise.close_connections()


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session")
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        print("Client is ready")
        yield client


@pytest.fixture(scope="session", autouse=True)
async def initialize_tests():
    async with register_orm(drop=True):
        yield
