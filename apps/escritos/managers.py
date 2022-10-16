import random
from typing import Type

from django.db.models import QuerySet, Count, F

from apps.general.constants import BASE_ESCRITO_PUBLISHED
from apps.general.managers import BaseManager


class TermQuerySet(QuerySet):
    def tags_category_prefetch(self):
        return self.prefetch_related(
            "category",
            "tags",
            "author",
        )

    def prefetch_all(self):
        return self.prefetch_related(
            "category",
            "tags",
            "author",
            "term_content_parts",
        )


class TermManager(BaseManager):
    def get_queryset(self):
        return TermQuerySet(self.model, using=self._db).prefetch_all()

    def get_random(self, query=None):
        query = query if query else self.all()
        models_list = list(query)
        return random.choice(models_list)

    def term_ready_newsletter(self) -> Type:
        return (
            self.filter_checkings("information_clean", True)
            .annotate(
                times_sent_email=Count("website_email"),
            )
            .order_by("-times_sent_email")
            .first()
        )

    def clean_terms(self):
        return self.filter(status=BASE_ESCRITO_PUBLISHED)

    def clean_terms_with_resume(self):
        return self.filter(status=BASE_ESCRITO_PUBLISHED, resume__isnull=False)

    def random_clean(self):
        return self.get_random(self.clean_terms_with_resume())
