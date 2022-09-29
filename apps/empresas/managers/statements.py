from django.db.models import Count, F, Manager, Q, Subquery, OuterRef, QuerySet

from apps.general import constants


class BaseStatementManager(Manager):
    def quarterly(self, **kwargs) -> QuerySet:
        return self.filter(~Q(period__period=constants.PERIOD_FOR_YEAR), **kwargs)

    def yearly(self, **kwargs) -> QuerySet:
        return self.filter(Q(is_ttm=True) | Q(period__period=constants.PERIOD_FOR_YEAR), **kwargs)

    def yearly_exclude_ttm(self, **kwargs) -> QuerySet:
        return self.filter(Q(is_ttm=False) | Q(period__period=constants.PERIOD_FOR_YEAR), **kwargs)
