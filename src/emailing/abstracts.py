from django.contrib.auth import get_user_model
from django.db.models import (
    CASCADE,
    SET_NULL,
    BooleanField,
    CharField,
    DateTimeField,
    ForeignKey,
    ManyToManyField,
    SlugField,
)
from django.utils import timezone

from ckeditor.fields import RichTextField

from src.general.abstracts import AbstractTimeStampedModel

from .extensions import EmailExtension

User = get_user_model()


class AbstractEmail(AbstractTimeStampedModel, EmailExtension):
    title = CharField(max_length=500)
    content = RichTextField(config_name="simple")
    default_title = ForeignKey(
        "content_creation.DefaultTilte",
        on_delete=SET_NULL,
        null=True,
        blank=True,
    )
    default_content = ForeignKey(
        "content_creation.DefaultContent",
        on_delete=SET_NULL,
        null=True,
        blank=True,
    )
    title_emojis = ManyToManyField("content_creation.Emoji", blank=True)
    sent = BooleanField(default=False)
    date_to_send = DateTimeField(null=True, blank=True)
    call_to_action = CharField(max_length=500, null=True, blank=True)
    call_to_action_url = CharField(max_length=500, null=True, blank=True)

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return self.title


class AbstractTrackEmail(AbstractTimeStampedModel):
    sent_to = ForeignKey(User, on_delete=CASCADE)
    date_sent = DateTimeField(auto_now_add=True)
    opened = BooleanField(default=False)
    date_opened = DateTimeField(default=timezone.now)

    class Meta:
        abstract = True
