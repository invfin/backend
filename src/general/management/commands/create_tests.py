from django.conf import settings
from django.core.management import BaseCommand

# from bfet import Autotest


class Command(BaseCommand):
    def handle(self, *args, **options):
        # mods = []
        # for m in sys.modules.keys():
        #     if m.startswith("src.seo"):
        #         mods.append(m)
        for local_app in settings.LOCAL_APPS:
            if "etfs" in local_app:
                continue
            # Autotest.start(app=local_app)
