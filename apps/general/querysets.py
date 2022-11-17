import random

from typing import Dict, List, Type, Optional

from django.db.models import QuerySet


class BaseQuerySet(QuerySet):
    # https://docs.djangoproject.com/en/3.2/topics/db/queries/#querying-jsonfield
    def filter_checking(self, checking: str, has_it: bool) -> QuerySet:
        state = "yes" if has_it else "no"
        return self.filter(**{f"checkings__has_{checking}__state": state})

    def filter_checking_not_seen(self, checking: str) -> QuerySet:
        return self.filter(**{f"checkings__has_{checking}__state": "no", f"checkings__has_{checking}__time": ""})

    def filter_checkings(self, list_checkings: List[Dict[str, bool]]) -> QuerySet:
        all_checkings = dict()
        for checking in list_checkings:
            for key, value in checking.items():
                state = "yes" if value else "no"
                all_checkings.update({f"checkings__has_{key}__state": state})

        return self.filter(**all_checkings)

    def get_random(self, query: QuerySet = None) -> Optional[Type]:
        query = query if query else self.all()
        models_list = list(query)
        return random.choice(models_list) if models_list else None
