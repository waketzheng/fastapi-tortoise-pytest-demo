from tortoise import fields, migrations
from tortoise.migrations import operations as ops


class Migration(migrations.Migration):
    initial = True

    operations = [
        ops.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    fields.IntField(
                        generated=True, primary_key=True, unique=True, db_index=True
                    ),
                ),
                ("username", fields.CharField(unique=True, max_length=60)),
                ("age", fields.IntField(null=True)),
            ],
            options={"table": "users", "app": "models", "pk_attr": "id"},
            bases=["Model"],
        ),
    ]
