from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator

from .base import AbsModel, fields


class User(AbsModel):
    username = fields.CharField(60)
    age = fields.IntField()

    class Meta:
        table = "users"

    def __str__(self):
        return self.name


User_Pydantic = pydantic_model_creator(User)
UserIn_Pydantic = pydantic_model_creator(User, name="UserIn", exclude_readonly=True)
User_Pydantic_List = pydantic_queryset_creator(User)
