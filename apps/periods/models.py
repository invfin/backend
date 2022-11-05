from django.contrib.auth import get_user_model
from django.db.models import (
    CASCADE,
    SET_NULL,
    BooleanField,
    CharField,
    ForeignKey,
    IntegerField,
    ManyToManyField,
    Model,
)

from apps.periods.constants import PERIODS
from apps.general.abstracts import AbstractTimeStampedModel
from apps.periods.managers import PeriodManager


User = get_user_model()


class Period(AbstractTimeStampedModel):
    year = IntegerField(null=True, blank=True)
    period = IntegerField(choices=PERIODS, null=True, blank=True)
    objects = PeriodManager()

    class Meta:
        verbose_name = "Period"
        verbose_name_plural = "Periods"
        db_table = "assets_periods"
        ordering = ["-year", "-period"]
        get_latest_by = ["-year", "-period"]

    def __str__(self):
        if self.is_full_year:
            return f"FY {str(self.period_year)}"
        return f"Q{self.period} {str(self.period_year)}"

    @property
    def is_full_year(self):
        return self.period == constants.PERIOD_FOR_YEAR

    @property
    def period_year(self):
        return self.year
