from django.db.models import Manager
from general.querysets import BaseQuerySet


class BaseManager(Manager.from_queryset(BaseQuerySet)):
    pass
