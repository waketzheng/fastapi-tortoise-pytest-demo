from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models.users import User, User_Pydantic, User_Pydantic_List, UserIn_Pydantic
from settings import ALLOW_ORIGINS, DB_URL
from tortoise.contrib.fastapi import register_tortoise

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/testpost", response_model=User_Pydantic)
async def world(user: UserIn_Pydantic):
    return await User.create(**user.dict())


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
