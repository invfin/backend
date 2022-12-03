from django.db.models import Manager

from src.web.querysets import RoadmapQuerySet


class RoadmapManager(Manager.from_queryset(RoadmapQuerySet)):
    pass
