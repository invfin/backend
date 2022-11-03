from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db.models import (
    CASCADE,
    SET_NULL,
    BooleanField,
    CharField,
    ForeignKey,
    DateTimeField,
    ManyToManyField,
)

from ckeditor.fields import RichTextField

from apps.general.abstracts import AbstractTimeStampedModel


User = get_user_model()


class AbstractEmail(AbstractTimeStampedModel):
    title = CharField(max_length=500)
    content = RichTextField(config_name="simple")
    default_title = ForeignKey(
        "socialmedias.DefaultTilte",
        on_delete=SET_NULL,
        null=True,
        blank=True,
    )
    default_content = ForeignKey(
        "socialmedias.DefaultContent",
        on_delete=SET_NULL,
        null=True,
        blank=True,
    )
    title_emojis = ManyToManyField("socialmedias.Emoji", blank=True)
    sent = BooleanField(default=False)
    date_to_send = DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

    @property
    def email_serialized(self):
        return {
            "subject": self.title,
            "content": self.content,
            **self.dict_for_task,
        }

    @property
    def opening_rate(self):
        all_emails = self.email_related.all().count()
        all_opened = self.email_related.filter(opened=True).count()
        rate = all_emails / all_opened if all_opened != 0 else 0
        return round(rate, 2)


class AbstractTrackEmail(AbstractTimeStampedModel):
    sent_to = ForeignKey(User, on_delete=CASCADE)
    date_sent = DateTimeField(auto_now_add=True)
    opened = BooleanField(default=False)
    date_opened = DateTimeField(default=timezone.now)

    class Meta:
        abstract = True
