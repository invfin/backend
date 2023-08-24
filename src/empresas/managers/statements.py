from django.db.models import Q

from src.empresas.querysets.statements import StatementQuerySet
from src.general.managers import BaseManager
from src.periods.constants import PERIOD_FOR_YEAR


class BaseStatementManager(BaseManager):
    def year(self):
        return self.select_related(
            "period",
            "reported_currency",
        ).filter(period__period=PERIOD_FOR_YEAR)

    def yearly(
        self,
        include_ttm: bool = True,
        **kwargs,
    ) -> "StatementQuerySet":
        if (
            yearly_filtered := self.get_queryset()
            .select_related("period", "reported_currency")
            .filter(
                Q(is_ttm=include_ttm) | Q(period__period=PERIOD_FOR_YEAR),
                **kwargs,
            )
        ):
            return yearly_filtered
        return self.get_queryset().all()

    def yearly_exclude_ttm(self) -> "StatementQuerySet":
        return self.yearly(False)
