from django.core.management import BaseCommand

from apps.empresas.tasks import fix_update_financials_task
from apps.empresas.models import Company


class Command(BaseCommand):
    def handle(self, *args, **options):
        for company in Company.objects.filter(ticker="AAPL"):
            fix_update_financials_task.delay(company.id)
