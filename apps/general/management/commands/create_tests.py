from django.core.management import BaseCommand
from django.conf import settings

from autotest.autotest import Autotest

class Command(BaseCommand):
    def handle(self, *args, **options):
        Autotest.start(app="apps.web")
        for local_app in settings.LOCAL_APPS[1:2]:
            print(local_app)
