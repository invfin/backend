import random

from django.db.models import Manager

from apps.general.constants import BASE_ESCRITO_PUBLISHED


class TermManager(Manager):
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
