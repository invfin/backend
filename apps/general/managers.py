import random
from typing import Dict, List, Type, Optional

from django.db.models import Manager, QuerySet

from apps.general import constants


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


class BaseManager(Manager):
    def get_queryset(self):
        return BaseQuerySet(self.model, using=self._db)

    def filter_checkings(self, checkings: List[Dict[str, bool]]) -> QuerySet:
        return self.get_queryset().filter_checkings(checkings)

    def filter_checking(self, checking: str, has_it: bool) -> QuerySet:
        return self.get_queryset().filter_checking(checking, has_it)

    def filter_checking_not_seen(self, checking: str) -> QuerySet:
        return self.get_queryset().filter_checking_not_seen(checking)

    def get_random(self, query: QuerySet = None) -> Optional[Type]:
        query = query if query else self.all()
        models_list = list(query)
        return random.choice(models_list) if models_list else None


class CurrencyManager(Manager):
    def financial_currency(self, currency) -> Type:
        currency, created = self.get_or_create(currency=currency)
        return currency


class PeriodManager(Manager):
    def for_year_period(self, year) -> Type:
        period, created = self.get_or_create(year=year, period=constants.PERIOD_FOR_YEAR)
        return period

    def first_quarter_period(self, year) -> Type:
        period, created = self.get_or_create(year=year, period=constants.PERIOD_1_QUARTER)
        return period

    def second_quarter_period(self, year) -> Type:
        period, created = self.get_or_create(year=year, period=constants.PERIOD_2_QUARTER)
        return period

    def third_quarter_period(self, year) -> Type:
        period, created = self.get_or_create(year=year, period=constants.PERIOD_3_QUARTER)
        return period

    def fourth_quarter_period(self, year) -> Type:
        period, created = self.get_or_create(year=year, period=constants.PERIOD_4_QUARTER)
        return period

    def quarterly_periods(self) -> QuerySet:
        return self.all().exclude(period=constants.PERIOD_FOR_YEAR)

    def yearly_periods(self) -> QuerySet:
        return self.filter(period=constants.PERIOD_FOR_YEAR)
