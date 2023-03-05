from typing import Type

from django.db.models import Count, QuerySet

from src.escritos.constants import BASE_ESCRITO_PUBLISHED
from src.general.managers import BaseManager, BaseQuerySet


class TermQuerySet(BaseQuerySet):
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

    def to_be_cleaned(self):
        return self.filter(
            status=BASE_ESCRITO_PUBLISHED,
            **{
                "checkings__has_information_clean__state": "no",
                "checkings__has_request_improvement__state": "no",
            },
        ).order_by("total_views")

    def cleaning_requested(self):
        return self.filter(
            **{
                "checkings__has_information_clean__state": "no",
                "checkings__has_request_improvement__state": "yes",
            }
        )

    def all_terms_ready_newsletter(self) -> QuerySet:
        return (
            self.filter_checking("information_clean", True)
            .annotate(
                times_sent_email=Count("website_email"),
            )
            .order_by("-times_sent_email")
        )

    def term_ready_newsletter(self) -> Type:
        return self.get_random(self.all_terms_ready_newsletter())

    def clean_terms(self):
        return self.filter(status=BASE_ESCRITO_PUBLISHED)

    def clean_terms_with_resume(self):
        return self.filter(status=BASE_ESCRITO_PUBLISHED, resume__isnull=False)

    def random_clean(self):
        return self.get_random(self.clean_terms_with_resume())
