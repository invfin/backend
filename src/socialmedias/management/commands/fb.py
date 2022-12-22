from django.conf import settings
from django.core.management import BaseCommand

from src.socialmedias.outils.socialposter.tweetpy import Twitter


class Command(BaseCommand):
    def handle(self, *args, **options):
        post_content = dict(
            media="/static/general/assets/img/general/why-us.webp",
            title="Default title",
            content="Default content #default #hashtags",
            hashtags="",
            post_type=2,
            link="https://inversionesyfinanzas.xyz",
        )
        fb_response = Twitter(
            settings.TWITTER_CONSUMER_KEY,
            settings.TWITTER_CONSUMER_SECRET,
            settings.TWITTER_ACCESS_TOKEN,
            settings.TWITTER_ACCESS_TOKEN_SECRET,
        ).post(**post_content)
        print(fb_response)
