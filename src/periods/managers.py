from django.db.models import Manager

from . import constants


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
        return self.exclude(period=constants.PERIOD_FOR_YEAR)

    def yearly_periods(self):
        return self.filter(period=constants.PERIOD_FOR_YEAR)
