import random

from django.db.models import Manager, QuerySet

from apps.general.constants import BASE_ESCRITO_PUBLISHED


class TermQuerySet(QuerySet):
    def tags_category_prefetch(self):
        return self.prefetch_related(
            "category",
            "tags",
            "author",
        )


class TermManager(Manager):
    def get_queryset(self):
        return TermQuerySet(self.model, using=self._db).tags_category_prefetch()

    def get_random(self, query=None):
        query = query if query else self.all()
        models_list = list(query)
        return random.choice(models_list)

    def clean_terms(self):
        return self.filter(status=BASE_ESCRITO_PUBLISHED)

    def clean_terms_with_resume(self):
        return self.filter(status=BASE_ESCRITO_PUBLISHED, resume__isnull=False)

    def random_clean(self):
        return self.get_random(self.clean_terms_with_resume())
