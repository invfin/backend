from apps.general.managers import BaseManager
from apps.empresas.querysets import BaseStatementQuerySet


class BaseStatementManager(BaseManager.from_queryset(BaseStatementQuerySet)):
    pass


class AsReportedStatementManager(BaseStatementManager):
    def get_queryset(self):
        return super().get_queryset().select_related("period", "company").prefetch_related("fields", "fields__concept")
