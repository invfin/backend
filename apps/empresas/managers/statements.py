from django.db.models import Count, F, Manager, Q, Subquery, OuterRef, QuerySet

from apps.general import constants


class BaseStatementManager(Manager):
    def quarterly(self, **kwargs) -> QuerySet:
        return self.filter(~Q(period__period=constants.PERIOD_FOR_YEAR), **kwargs)

    def yearly(self, **kwargs) -> QuerySet:
        yearly_filtered = self.filter(Q(is_ttm=True) | Q(period__period=constants.PERIOD_FOR_YEAR), **kwargs)
        if yearly_filtered.exists():
            return yearly_filtered
        else:
            if kwargs:
                return self.filter(**kwargs)
            else:
                return self.all()

    def yearly_exclude_ttm(self, **kwargs) -> QuerySet:
        return self.filter(Q(is_ttm=False) | Q(period__period=constants.PERIOD_FOR_YEAR), **kwargs)
