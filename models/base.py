from typing import List, Set, Tuple, Union

from tortoise import fields, models
from tortoise.queryset import Q, QuerySet


def reduce_query_filters(args: Tuple[Q, ...]) -> Set:
    fields = set()
    for q in args:
        fields |= set(q.filters)
        c: Union[List[Q], Tuple[Q, ...]] = q.children
        while c:
            _c: List[Q] = []
            for i in c:
                fields |= set(i.filters)
                _c += list(i.children)
            c = _c
    return fields


class AbsModel(models.Model):
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
        if not args or (field not in reduce_query_filters(args)):
            kwargs.setdefault(field, False)
        return super().filter(*args, **kwargs)

    class PydanticMeta:
        exclude = ("created_at", "updated_at", "is_deleted")

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.id}>"
