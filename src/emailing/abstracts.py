from django.contrib.auth import get_user_model
from django.db.models import CASCADE, SET_NULL, BooleanField, CharField, DateTimeField, ForeignKey, ManyToManyField
from django.utils import timezone

from ckeditor.fields import RichTextField

from src.general.abstracts import AbstractTimeStampedModel

User = get_user_model()


class AbstractEmail(AbstractTimeStampedModel):
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

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return self.title

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
