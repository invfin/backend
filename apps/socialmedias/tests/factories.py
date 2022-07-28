from factory import SubFactory
from factory.django import DjangoModelFactory

from apps.socialmedias.models import DefaultTilte, Emoji, Hashtag
from apps.socialmedias.tests.data import IG_HASHTAGS, ICONS, FB_HASHTAGS, TWITTER_HASHTAGS


class SocialmediaExamples:
    def create_hashtags():
        ig = [Hashtag(
                title=hashtag,
                platform='instagram'
        ) for hashtag in IG_HASHTAGS]
        fb = [Hashtag(
            title=hashtag,
            platform='facebook'
        ) for hashtag in FB_HASHTAGS]
        tw = [Hashtag(
            title=hashtag,
            platform='twitter'
        ) for hashtag in TWITTER_HASHTAGS]
        hashtags = ig + tw + fb
        Hashtag.objects.bulk_create(hashtags)
        
    def create_emojis(self):
        Emoji.objects.bulk_create([Emoji(emoji=emoji) for emoji in ICONS])
