from django.db.models import Count, F, Manager, Q, Subquery, OuterRef, QuerySet

from apps.general import constants


class BaseStatementQuerySet(QuerySet):
    pass


class BaseStatementManager(Manager):
    def get_queryset(self) -> QuerySet:
        return BaseStatementQuerySet(self.model, using=self._db)

    def quarterly(self) -> QuerySet:
        return self.filter(~Q(period__period=constants.PERIOD_FOR_YEAR))

    def yearly(self) -> QuerySet:
        return self.filter(Q(is_ttm=True) | Q(period__period=constants.PERIOD_FOR_YEAR))
