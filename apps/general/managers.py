import random
from typing import Dict, List, Type, Optional

from django.db.models import Manager, QuerySet
from general.querysets import BaseQuerySet


class BaseManager(Manager.from_queryset(BaseQuerySet)):
    pass
