from django.core.management import BaseCommand

# from src.empresas.tasks import launch_fix_update_financials_task


class Command(BaseCommand):
    def handle(self, *args, **options):
        pass
        # launch_fix_update_financials_task.delay()
