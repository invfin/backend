import random

from django.db.models import Manager, QuerySet

from apps.general import constants


class BaseManager(Manager):
    def filter_checkings(self, check: str, has_it: bool) -> QuerySet:
        checking = f"has_{check}"
        state = "yes" if has_it else "no"
        return self.filter(**{f"checkings__{checking}__state": state})

    def filter_checkings_not_seen(self, check: str) -> QuerySet:
        return self.filter(**{f"checkings__has_{check}__state": "no", f"checkings__has_{check}__time": ""})

    def get_random(self, query=None):
        query = query if query else self.all()
        models_list = list(query)
        return random.choice(models_list) if models_list else models_list


class CurrencyManager(Manager):
    def financial_currency(self, currency):
        currency, created = self.get_or_create(currency=currency)
        return currency


class PeriodManager(Manager):
    def for_year_period(self, year):
        period, created = self.get_or_create(year=year, period=constants.PERIOD_FOR_YEAR)
        return period

    def first_quarter_period(self, year):
        period, created = self.get_or_create(year=year, period=constants.PERIOD_1_QUARTER)
        return period

    def second_quarter_period(self, year):
        period, created = self.get_or_create(year=year, period=constants.PERIOD_2_QUARTER)
        return period

    def third_quarter_period(self, year):
        period, created = self.get_or_create(year=year, period=constants.PERIOD_3_QUARTER)
        return period

    def fourth_quarter_period(self, year):
        period, created = self.get_or_create(year=year, period=constants.PERIOD_4_QUARTER)
        return period

    def quarterly_periods(self):
        return self.all().exclude(period=constants.PERIOD_FOR_YEAR)

    def yearly_periods(self):
        return self.filter(period=constants.PERIOD_FOR_YEAR)
