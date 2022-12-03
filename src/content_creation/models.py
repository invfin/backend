from django.contrib.auth import get_user_model
from django.db.models import BooleanField, CharField, Model, PositiveIntegerField, TextField

from ckeditor.fields import RichTextField

from src.general.mixins import BaseToAllMixin
from src.socialmedias.constants import SOCIAL_MEDIAS
from src.web import constants as web_constants

from .constants import ALL, FOR_CONTENT
from .managers import DefaultContentManager, EmojisManager, HashtagsManager, TitlesManager

User = get_user_model()


class Hashtag(Model, BaseToAllMixin):
    title = TextField(default="")
    platform = CharField(max_length=500, choices=SOCIAL_MEDIAS)
    is_trending = BooleanField(default=False)
    objects = HashtagsManager()

    class Meta:
        verbose_name = "Default hashtags"
        db_table = "socialmedia_hashtags"

    def __str__(self) -> str:
        return str(self.title)


class Emoji(Model, BaseToAllMixin):
    emoji = CharField(max_length=500)
    objects = EmojisManager()

    class Meta:
        verbose_name = "Default emojis"
        db_table = "socialmedia_emojis"

    def __str__(self) -> str:
        return str(self.emoji)


class DefaultTilte(Model, BaseToAllMixin):
    title = TextField(default="")
    for_content = PositiveIntegerField(choices=FOR_CONTENT, blank=True, default=ALL)
    purpose = CharField(max_length=500, choices=web_constants.CONTENT_PURPOSES, null=True, blank=True)
    objects = TitlesManager()

    class Meta:
        verbose_name = "Default titles"
        db_table = "socialmedia_titles"

    def __str__(self) -> str:
        return str(self.title)


class DefaultContent(Model, BaseToAllMixin):
    title = CharField(max_length=500)
    for_content = PositiveIntegerField(choices=FOR_CONTENT, blank=True, default=ALL)
    purpose = CharField(max_length=500, choices=web_constants.CONTENT_PURPOSES, null=True, blank=True)
    content = RichTextField()
    objects = DefaultContentManager()

    class Meta:
        verbose_name = "Default content"
        db_table = "socialmedia_content"

    def __str__(self) -> str:
        return str(self.title)
