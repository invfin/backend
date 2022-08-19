from django.core.management import BaseCommand

from apps.empresas.models import CompanyUpdateLog


class Command(BaseCommand):
    def handle(self, *args, **options):
        CompanyUpdateLog.objects.all().delete()
