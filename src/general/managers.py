import random
from typing import Dict, List

from django.db.models import Manager, QuerySet

from .querysets import BaseQuerySet


class BaseManager(Manager.from_queryset(BaseQuerySet)):
    def filter_checkings(self, checkings: List[Dict[str, bool]]):
        return super().filter_checkings(checkings)

    def filter_checking(self, checking: str, has_it: bool):
        return super().filter_checking(checking, has_it)

    def filter_checking_not_seen(self, checking: str):
        return super().filter_checking_not_seen(checking)

    def get_random(self, query: QuerySet = None):
        query = query if query else self.all()
        models_list = list(query)
        return random.choice(models_list) if models_list else None
