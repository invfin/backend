from django.contrib.auth import get_user_model
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        User = get_user_model()
        u_1 = User.objects.get(id=1)
        u_1.set_password("tete2323")
        u_1.save()
