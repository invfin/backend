from apps.socialmedias.models import DefaultTilte, Emoji, Hashtag
from apps.socialmedias.tests.data import EMOJIS, DEFAULT_TITLES, HASHTAGS


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