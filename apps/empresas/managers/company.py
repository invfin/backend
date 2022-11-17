from typing import Any, Dict, Type

from django.db.models import Count, F, Manager, Prefetch, Q, QuerySet

from apps.general.managers import BaseManager
from apps.empresas.querysets import CompanyQuerySet


class CompanyManager(BaseManager.from_queryset(CompanyQuerySet)):
    pass


class AsReportedManager(CompanyManager):
    def get_queryset(self):
        return super().get_queryset().prefetch_as_reported()


class CompanyUpdateLogManager(Manager):
    pass
