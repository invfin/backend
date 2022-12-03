from django.db.models import Q, QuerySet

from src.general.managers import BaseManager, BaseQuerySet
from src.periods import constants


class BaseStatementQuerySet(BaseQuerySet):
    def quarterly(self):
        return self.exclude(period__period=constants.PERIOD_FOR_YEAR)

    def yearly(self):
        return self.filter(period__period=constants.PERIOD_FOR_YEAR)


class BaseStatementManager(BaseManager):
    def get_queryset(self):
        return BaseStatementQuerySet(self.model, using=self._db)

    def quarterly(self, **kwargs):
        return self.get_queryset().quarterly(**kwargs)

    def yearly(self, include_ttm: bool = True, **kwargs):
        yearly_filtered = self.filter(Q(is_ttm=include_ttm) | Q(period__period=constants.PERIOD_FOR_YEAR), **kwargs)
        if yearly_filtered:
            return yearly_filtered
        else:
            if kwargs:
                return self.filter(**kwargs)
            else:
                return self.all()

    def yearly_exclude_ttm(self, **kwargs):
        return self.yearly(False, **kwargs)
