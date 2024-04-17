#!/usr/bin/env python
from pathlib import Path
from typing import List

import fastapi_cdn_host
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise

from models.users import User, UserIn_Pydantic, UserPydantic
from settings import ALLOW_ORIGINS, DB_URL

app = FastAPI()
fastapi_cdn_host.monkey_patch(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/testpost", response_model=UserPydantic)
async def world(user: UserIn_Pydantic):  # type:ignore[valid-type]
    data = user.model_dump(exclude_unset=True)  # type:ignore[attr-defined]
    user_obj = await User.create(**data)
    # 2024.04.17 raises ValidationError:
    """
    E   pydantic_core._pydantic_core.ValidationError: 1 validation error for User
    E   Meta
    E     Extra inputs are not permitted [type=extra_forbidden, input_value=<class 'tortoise.models.Model.Meta'>, input_type=type]
    E       For further information visit https://errors.pydantic.dev/2.7/v/extra_forbidden
    """
    # return await User_Pydantic.from_tortoise_orm(user_obj)
    return UserPydantic(id=user_obj.id, username=user_obj.username, age=user_obj.age)


@app.get("/users", response_model=List[UserPydantic])
async def user_list():
    user_objs = await User.all()
    return [
        UserPydantic(id=user_obj.id, username=user_obj.username, age=user_obj.age)
        for user_obj in user_objs
    ]


register_tortoise(
    app,
    config={
        "connections": {"default": DB_URL},
        "apps": {"models": {"models": ["models"]}},
        "use_tz": True,
        "timezone": "Asia/Shanghai",
        "generate_schemas": True,
    },
)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(f"{Path(__file__).stem}:app")
