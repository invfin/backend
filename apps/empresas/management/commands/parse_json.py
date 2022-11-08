from django.core.management import BaseCommand

from apps.empresas.parse.parse_json import main


class Command(BaseCommand):
    def handle(self, *args, **options):
        main()
