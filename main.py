#!/usr/bin/env python
from __future__ import annotations

import subprocess

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise

from models.users import User, User_Pydantic, UserIn_Pydantic
from settings import ALLOW_ORIGINS, TORTOISE_ORM

app = FastAPI()
register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=True,
    add_exception_handlers=True,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/testpost", response_model=User_Pydantic)
async def world(user: UserIn_Pydantic):
    data = user.model_dump(exclude_unset=True)
    user_obj = await User.create(**data)
    return await User_Pydantic.from_tortoise_orm(user_obj)


@app.get("/users", response_model=list[User_Pydantic])
async def user_list(name: str | None = None, age: int | None = None):
    qs = User.all()
    if name:
        qs = qs.filter(username__icontains=name)
    if age is not None:
        qs = qs.filter(age=age)
    return await User_Pydantic.from_queryset(qs)


if __name__ == "__main__":
    subprocess.run(["fastcdn", __file__, "--port=8000"])  # Run server in dev mode
