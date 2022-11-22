from django.contrib.auth import get_user_model
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        User = get_user_model()
        u_1 = User.objects.get(id=1)
        u2 = User.objects.get(username="Lluc")
        u_1.set_password("tete2323")
        u_1.save()
        u2.set_password("tete2323")
        u2.save()
