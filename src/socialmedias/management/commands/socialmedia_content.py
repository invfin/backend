from django.core.management import BaseCommand

from src.content_creation.models import Emoji, Hashtag
from src.socialmedias.test_socialmedias.data import FB_HASHTAGS, ICONS, IG_HASHTAGS, TWITTER_HASHTAGS


class Command(BaseCommand):
    def handle(self, *args, **options):
        ig = [Hashtag(title=hashtag, platform="instagram") for hashtag in IG_HASHTAGS]
        fb = [Hashtag(title=hashtag, platform="facebook") for hashtag in FB_HASHTAGS]
        tw = [Hashtag(title=hashtag, platform="twitter") for hashtag in TWITTER_HASHTAGS]
        emojis = [Emoji(emoji=emoji) for emoji in ICONS]
        hashtags = ig + tw + fb
        Hashtag.objects.bulk_create(hashtags)
        Emoji.objects.bulk_create(emojis)
