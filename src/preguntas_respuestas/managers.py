import random

from django.db.models import Count, Manager


class QuestionManager(Manager):
    def get_random(self, query=None):
        models_list = list(query or self.all())
        return random.choice(models_list) if models_list else models_list

    def single_api_query(self):
        return (
            self.prefetch_related(
                "upvotes",
                "tags",
                "downvotes",
                "answers",
                "comments_related",
                "answers__comments_related",
            )
            .select_related("author", "category")
            .annotate(
                total_upvotes=Count("upvotes"),
                total_downvotes=Count("downvotes"),
            )
        )

    def many_api_query(self):
        return (
            self.prefetch_related(
                "upvotes",
                "tags",
                "downvotes",
            )
            .select_related("author", "category")
            .annotate(
                total_upvotes=Count("upvotes"),
                total_downvotes=Count("downvotes"),
            )
        )
