from django.core.management import BaseCommand

from src.empresas.models import CompanyUpdateLog


class Command(BaseCommand):
    def handle(self, *args, **options):
        CompanyUpdateLog.objects.filter(error_message="Works great").delete()
