from django.core.management import BaseCommand

from apps.empresas.models import Company


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('checking', type=str)

    def handle(self, *args, **options):
        checking = options['checking']
        for company in Company.objects.all():
            company.checkings.update(
                {
                    f'has_{checking}': {
                        'state': 'no',
                        'time': ''
                    }
                }
            )
            company.save(update_fields=["checkings"])
