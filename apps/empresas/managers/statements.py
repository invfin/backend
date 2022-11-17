from apps.general.managers import BaseManager
from apps.empresas.querysets import BaseStatementQuerySet


class BaseStatementManager(BaseManager.from_queryset(BaseStatementQuerySet)):
    pass
