from django.core.management import BaseCommand

from apps.empresas.models import Company
from apps.general.utils import add_new_default_check
from apps.empresas.constants import DEFAULT_JSON_CHECKS_FILE


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("checking", type=str)

    def handle(self, *args, **options):
        checking = options["checking"]
        add_new_default_check(checking, DEFAULT_JSON_CHECKS_FILE)
        for company in Company.objects.all():
            company.checkings.update({f"has_{checking}": {"state": "no", "time": ""}})
            company.save(update_fields=["checkings"])
