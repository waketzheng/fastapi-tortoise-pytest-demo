import pytest
from httpx import AsyncClient

from models.users import User


@pytest.mark.anyio
async def test_testpost(client: AsyncClient):
    name, age = "sam", 99
    assert await User.filter(username=name).count() == 0

    data = {"username": name, "age": age}
    response = await client.post("/testpost", json=data)
    assert response.json() == dict(data, id=1)
    assert response.status_code == 200

    response = await client.get("/users")
    assert response.status_code == 200
    assert response.json() == [dict(data, id=1)]

    assert await User.filter(username=name).count() == 1
