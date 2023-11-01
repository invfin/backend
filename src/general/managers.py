import random
from typing import Any, Dict, List, Optional

from django.db.models import Manager
from django.db.models.query import QuerySet


class BaseQuerySet(QuerySet):
    # https://docs.djangoproject.com/en/3.2/topics/db/queries/#querying-jsonfield
    def filter_checking(self, checking: str, has_it: bool):
        state = "yes" if has_it else "no"
        return self.filter(**{f"checkings__has_{checking}__state": state})

    def filter_checking_not_seen(self, checking: str):
        return self.filter(
            **{
                f"checkings__has_{checking}__state": "no",
                f"checkings__has_{checking}__time": "",
            },
        )

    def filter_checkings(self, list_checkings: List[Dict[str, bool]]):
        all_checkings = {}
        for checking in list_checkings:
            for key, value in checking.items():
                state = "yes" if value else "no"
                all_checkings[f"checkings__has_{key}__state"] = state
        return self.filter(**all_checkings)


class BaseManager(Manager):
    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset()

    def search(self, query):
        return self.all()

    def filter_checkings(self, checkings: List[Dict[str, bool]]) -> "BaseQuerySet":
        return self.get_queryset().filter_checkings(checkings)

    def filter_checking(self, checking: str, has_it: bool) -> "BaseQuerySet":
        return self.get_queryset().filter_checking(checking, has_it)

    def filter_checking_not_seen(self, checking: str) -> "BaseQuerySet":
        return self.get_queryset().filter_checking_not_seen(checking)

    def get_random(self, query: Optional[QuerySet] = None) -> Optional[type]:
        query = query or self.all()
        models_list = list(query)
        return random.choice(models_list) if models_list else None
