from django.db.models import Manager

from apps.general import constants


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
