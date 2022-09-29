from django.core.management import BaseCommand

from apps.empresas.tasks import launch_fix_update_financials_task


class Command(BaseCommand):
    def handle(self, *args, **options):
        launch_fix_update_financials_task.delay()
