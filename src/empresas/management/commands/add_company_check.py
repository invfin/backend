from django.core.management import BaseCommand

from src.empresas.constants import DEFAULT_JSON_CHECKS_FILE
from src.empresas.models import Company
from src.general.outils.bulk_json_field_update import AddChecking
from src.general.utils import add_new_default_check


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("checking", type=str)

    def handle(self, *args, **options):
        checking = options["checking"]
        add_new_default_check(checking, DEFAULT_JSON_CHECKS_FILE)
        Company.objects.all().update(checkings=AddChecking(checking))
