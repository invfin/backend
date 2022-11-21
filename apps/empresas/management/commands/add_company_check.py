from django.core.management import BaseCommand

from apps.empresas.models import Company
from apps.general.utils import add_new_default_check
from apps.empresas.constants import DEFAULT_JSON_CHECKS_FILE
from apps.general.outils.bulk_json_field_update import AddChecking


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("checking", type=str)

    def handle(self, *args, **options):
        checking = options["checking"]
        add_new_default_check(checking, DEFAULT_JSON_CHECKS_FILE)
        Company.objects.all().update(checkings=AddChecking(checking))
