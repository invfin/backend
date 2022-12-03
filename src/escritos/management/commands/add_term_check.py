from django.core.management import BaseCommand

from src.escritos.models import Term
from src.escritos.constants import DEFAULT_JSON_CHECKS_FILE
from src.general.utils import add_new_default_check


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("checking", type=str)

    def handle(self, *args, **options):
        checking = options["checking"]
        add_new_default_check(checking, DEFAULT_JSON_CHECKS_FILE)
        for term in Term.objects.all():
            term.checkings.update({f"has_{checking}": {"state": "no", "time": ""}})
            term.save(update_fields=["checkings"])
