from django.db.models import Manager, Q, QuerySet

from apps.periods import constants


class BaseStatementManager(Manager):
    def quarterly(self, **kwargs) -> QuerySet:
        return self.filter(~Q(period__period=constants.PERIOD_FOR_YEAR), **kwargs)

    def yearly(self, include_ttm: bool = True, **kwargs) -> QuerySet:
        yearly_filtered = self.filter(Q(is_ttm=include_ttm) | Q(period__period=constants.PERIOD_FOR_YEAR), **kwargs)
        if yearly_filtered:
            return yearly_filtered
        else:
            if kwargs:
                return self.filter(**kwargs)
            else:
                return self.all()

    def yearly_exclude_ttm(self, **kwargs) -> QuerySet:
        return self.yearly(False, **kwargs)
