from django.db.models import Q
from src.general.managers import BaseManager
from src.periods import constants

from src.empresas.querysets.statements import StatementQuerySet


class BaseStatementManager(BaseManager):
    def get_queryset(self) -> "StatementQuerySet":
        return super().get_queryset()

    def quarterly(
        self,
        include_ttm: bool = True,
        **kwargs,
    ) -> "StatementQuerySet":
        return self.get_queryset().filter(
            Q(is_ttm=include_ttm) | ~Q(period__period=constants.PERIOD_FOR_YEAR),
            **kwargs,
        )

    def yearly(
        self,
        include_ttm: bool = True,
        **kwargs,
    ) -> "StatementQuerySet":
        yearly_filtered = self.get_queryset().filter(
            Q(is_ttm=include_ttm) | Q(period__period=constants.PERIOD_FOR_YEAR),
            **kwargs,
        )
        if yearly_filtered:
            return yearly_filtered
        return self.get_queryset().all()

    def yearly_exclude_ttm(self) -> "StatementQuerySet":
        return self.yearly(False)

    def quarterly_exclude_ttm(self) -> "StatementQuerySet":
        return self.yearly(False)
