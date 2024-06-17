import pytest
from httpx import AsyncClient

from models.users import User


@pytest.mark.anyio
async def test_testpost(client: AsyncClient):
    name, age = "sam", 99
    assert await User.filter(username=name).count() == 0

    data = {"username": name, "age": age}
    user_data = dict(data, id=1)
    response = await client.post("/testpost", json=data)
    assert response.json() == user_data
    assert response.status_code == 200

    response = await client.get("/users")
    assert response.status_code == 200
    assert response.json() == [user_data]

    assert await User.filter(username=name).count() == 1

    user2 = await User.create(username="James", age=23)
    assert str(user2) == 'James'
    assert repr(user2) == '<User(id=2)>'
    user_data_2 = {"id": 2, "username": "James", "age": 23}
    response = await client.get("/users?name=james")
    assert response.status_code == 200
    assert response.json() == [user_data_2]
    response = await client.get("/users?age=99")
    assert response.status_code == 200
    assert response.json() == [user_data]
    response = await client.get("/users?name=am")
    assert response.status_code == 200
    assert response.json() == [user_data, user_data_2]
