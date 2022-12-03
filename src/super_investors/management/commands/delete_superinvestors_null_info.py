from django.core.management import BaseCommand

from src.super_investors.models import SuperinvestorActivity, SuperinvestorHistory


class Command(BaseCommand):
    def handle(self, *args, **options):
        SuperinvestorActivity.objects.filter(superinvestor_related__isnull=True).delete()
        SuperinvestorHistory.objects.filter(superinvestor_related__isnull=True).delete()
