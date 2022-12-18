from django.db.models import QuerySet


class SocialmediaAuthQuerySet(QuerySet):
    def get_user_socialmedias(self, user: type):
        return self.filter(user=user)
