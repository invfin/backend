from django.db.models import Manager

from apps.web.querysets import RoadmapQuerySet


class RoadmapManager(Manager.from_queryset(RoadmapQuerySet)):
    pass
