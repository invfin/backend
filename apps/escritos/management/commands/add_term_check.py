from django.core.management import BaseCommand

from apps.escritos.models import Term
from apps.escritos.constants import DEFAULT_JSON_CHECKS_FILE
from apps.general.utils import add_new_default_check


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("checking", type=str)

    def handle(self, *args, **options):
        checking = options["checking"]
        add_new_default_check(checking, DEFAULT_JSON_CHECKS_FILE)
        for company in Term.objects.all():
            company.checkings.update({f"has_{checking}": {"state": "no", "time": ""}})
            company.save(update_fields=["checkings"])
