from django.db.models import Manager


class VisiteurManager(Manager):
    def real_visiteur(self):
        return self.filter(is_bot=False)
