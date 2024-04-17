from pydantic import BaseModel
from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class User(models.Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(60)
    age = fields.IntField()

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.id})>"


User_Pydantic = pydantic_model_creator(User)
UserIn_Pydantic = pydantic_model_creator(User, name="UserIn", exclude_readonly=True)


class UserPydantic(BaseModel):
    id: int
    username: str
    age: int
