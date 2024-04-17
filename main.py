#!/usr/bin/env python
from pathlib import Path

import fastapi_cdn_host
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise

from models.users import User, User_Pydantic, User_Pydantic_List, UserIn_Pydantic
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


@app.post("/testpost", response_model=User_Pydantic)
async def world(user: UserIn_Pydantic):
    return await User.create(**user.model_dump())


@app.get("/users", response_model=User_Pydantic_List)
async def user_list():
    return await User.all()


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
    uvicorn.run(f"{Path(__file__).stem}:app")
