from django.core.management import BaseCommand
from django.conf import settings
import sys
from autotest.autotest import Autotest

class Command(BaseCommand):
    def handle(self, *args, **options):
        
        # mods = []
        # for m in sys.modules.keys():
        #     if m.startswith("apps.seo"):
        #         mods.append(m)
        # print(mods)
        for local_app in settings.LOCAL_APPS:
            if "etfs" in local_app:
                continue
            Autotest.start(app=local_app)
