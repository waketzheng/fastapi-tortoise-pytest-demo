from tortoise import fields, models
from tortoise.queryset import QuerySet


class CoreModel(models.Model):
    id = fields.IntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True, description="Created At")
    updated_at = fields.DatetimeField(auto_now=True, description="Updated At")
    is_deleted = fields.BooleanField(default=False, description="Mark as Deleted")

    class Meta:
        abstract = True
        ordering = ("-id",)

    @classmethod
    def filter(cls, *args, **kwargs) -> QuerySet:
        field = "is_deleted"
        if not args or (
            (query_fields := [k for q in args for k in getattr(q, "filters", {})])
            and field not in query_fields
        ):
            kwargs.setdefault(field, False)
        return super().filter(*args, **kwargs)

    class PydanticMeta:
        exclude = ("created_at", "updated_at", "is_deleted")

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.id}>"
