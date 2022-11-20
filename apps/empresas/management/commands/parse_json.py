from django.core.management import BaseCommand

from apps.empresas.parse.parse_json import main, update_final


class Command(BaseCommand):
    def handle(self, *args, **options):
        # main()
        update_final()
