from __future__ import annotations

from typing import TYPE_CHECKING

from tortoise import Model, fields
from tortoise.contrib.pydantic import PydanticModel, pydantic_model_creator


class User(Model):
    id = fields.IntField(primary_key=True)
    username = fields.CharField(max_length=60, unique=True)
    age = fields.IntField(null=True)

    class Meta:
        db_table = "users"

    def __str__(self) -> str:
        return self.username

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(id={self.id})>"


if TYPE_CHECKING:

    class UserIn_Pydantic(User, PydanticModel):  # type:ignore[misc]
        pass

    class User_Pydantic(User, PydanticModel):  # type:ignore[misc]
        pass

else:
    User_Pydantic = pydantic_model_creator(User)
    UserIn_Pydantic = pydantic_model_creator(User, name="UserIn", exclude_readonly=True)
