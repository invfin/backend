from django.core.management import BaseCommand

from ...tasks import socialmedia_share_news


class Command(BaseCommand):
    def handle(self, *args, **options):
        socialmedia_share_news()
