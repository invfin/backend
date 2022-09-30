from apps.socialmedias.models import DefaultTilte, Emoji, Hashtag
from tests.test_socialmedias.data import IG_HASHTAGS, ICONS, FB_HASHTAGS, TWITTER_HASHTAGS


class SocialmediaExamples:
    def create_hashtags():
        ig = [Hashtag(title=hashtag, platform="instagram") for hashtag in IG_HASHTAGS]
        fb = [Hashtag(title=hashtag, platform="facebook") for hashtag in FB_HASHTAGS]
        tw = [Hashtag(title=hashtag, platform="twitter") for hashtag in TWITTER_HASHTAGS]
        hashtags = ig + tw + fb
        Hashtag.objects.bulk_create(hashtags)

    def create_emojis(self):
        Emoji.objects.bulk_create([Emoji(emoji=emoji) for emoji in ICONS])


from tests.test_socialmedias.data import EMOJIS, DEFAULT_TITLES, HASHTAGS


class GenerateSocialmediasExample:
    all_titles = DefaultTilte.objects.all()
    all_emojis = Emoji.objects.all()
    all_hashtags = Hashtag.objects.all()

    @classmethod
    def generate_default_title(cls):
        for info in DEFAULT_TITLES:
            DefaultTilte.objects.create(**info)

    @classmethod
    def generate_emoji(cls):
        for info in EMOJIS:
            Emoji.objects.create(**info)

    @classmethod
    def generate_hashtag(cls):
        for info in HASHTAGS:
            Hashtag.objects.create(**info)

    @classmethod
    def generate_all(cls):
        cls.generate_default_title()
        cls.generate_emoji()
        cls.generate_hashtag()
