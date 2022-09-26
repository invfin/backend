from django.db.models import Count, F, Manager, Q, Subquery, OuterRef, QuerySet

from apps.general import constants


class BaseStatementQuerySet(QuerySet):
    def quarterly(self) -> QuerySet:
        return self.filter(~Q(period__period=constants.PERIOD_FOR_YEAR))

    def yearly(self) -> QuerySet:
        return self.filter(Q(is_ttm=True) | Q(period__period=constants.PERIOD_FOR_YEAR))


class BaseStatementManager(Manager):
    def get_queryset(self) -> QuerySet:
        return BaseStatementQuerySet(self.model, using=self._db)

    def quarterly(self, **kwargs) -> QuerySet:
        return self.get_queryset().quarterly().filter(**kwargs)

    def yearly(self, **kwargs) -> QuerySet:
        return self.get_queryset().yearly().filter(**kwargs)
