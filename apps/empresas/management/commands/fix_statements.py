from django.core.management import BaseCommand

from apps.empresas.tasks import update_fix_statemenets_populate_finprep, create_averages_task
from apps.empresas.models import Company


class Command(BaseCommand):
    def handle(self, *args, **options):
        # update_fix_statemenets_populate_finprep.delay()
        create_averages_task(Company.objects.get(ticker="AAPL").id)
