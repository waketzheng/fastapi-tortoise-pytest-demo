from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class User(models.Model):
    id = fields.IntField(primary_key=True)
    username = fields.CharField(max_length=60)
    age = fields.IntField()

    def __str__(self):
        return self.username

    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.id})>"


User_Pydantic = pydantic_model_creator(User)
UserIn_Pydantic = pydantic_model_creator(User, name="UserIn", exclude_readonly=True)
