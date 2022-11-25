from django.db.models import QuerySet


class RoadmapQuerySet(QuerySet):
    def all(self):
        return super().all().order_by("-updated_at", "-created_at", "points")
