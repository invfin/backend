from django.core.management import BaseCommand

from apps.empresas.models import Company
from apps.empresas.tasks import update_periods_current_average_statements, update_finprep_from_current

class Command(BaseCommand):
    def handle(self, *args, **options):
        for company in Company.objects.clean_companies():
            update_periods_current_average_statements.delay(company.id)
            update_finprep_from_current.delay(company.id)
