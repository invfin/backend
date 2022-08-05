import random

from django.db.models import Manager


class QuestionManager(Manager):
    def get_random(self, query=None):
        models_list = list(query if query else self.all())
        return random.choice(models_list)
