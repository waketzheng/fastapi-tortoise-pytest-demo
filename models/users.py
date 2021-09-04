from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator

from .base import CoreModel, fields


class User(CoreModel):
    username = fields.CharField(60)
    age = fields.IntField()

    class Meta:
        table = "users"

    def __str__(self):
        return self.name


# model_fields = tuple(User._meta.fields)
# UserPy = pydantic_model_creator(User, include=model_fields)
# UserPy_List = pydantic_queryset_creator(User, include=model_fields)
User_Pydantic = pydantic_model_creator(User)
UserIn_Pydantic = pydantic_model_creator(User, name="UserIn", exclude_readonly=True)
User_Pydantic_List = pydantic_queryset_creator(User)
