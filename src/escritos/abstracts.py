from typing import List

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericRelation
from django.db.models import (
    SET_NULL,
    BooleanField,
    CharField,
    DateTimeField,
    ForeignKey,
    ImageField,
    IntegerField,
    JSONField,
    ManyToManyField,
    PositiveIntegerField,
    SlugField,
    TextField,
)

from src.classifications.models import Tag
from src.escritos import constants
from src.general.abstracts import AbstractTimeStampedModel
from src.general.mixins import CheckingsMixin, CommentsMixin, VotesMixin

User = get_user_model()


def default_dict():
    return constants.DEFAULT_EXTRA_DATA_DICT


class AbstractWrittenContent(AbstractTimeStampedModel, CommentsMixin, VotesMixin, CheckingsMixin):
    author = ForeignKey(User, on_delete=SET_NULL, null=True)
    title = CharField(max_length=800, null=True, blank=True)
    slug = SlugField(max_length=800, null=True, blank=True)
    category = ForeignKey(
        "classifications.Category",
        on_delete=SET_NULL,
        blank=True,
        null=True,
    )
    tags = ManyToManyField("classifications.Tag", blank=True)
    checkings = JSONField(default=default_dict)
    total_votes = IntegerField(default=0)
    total_views = PositiveIntegerField(default=0)
    times_shared = PositiveIntegerField(default=0)
    website_email = GenericRelation(
        "web.WebsiteEmail",
        related_query_name="website_email",
    )
    # notifications = GenericRelation("general.Notification")

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.save_unique_field("slug", self.title)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def add_tags(self, tags: List[str]) -> None:
        tags = Tag.objects.get_content_tags(tags)
        self.tags.add(*tags)
        return None


class AbstractPublishableContent(AbstractWrittenContent):
    resume = TextField(default="")
    published_at = DateTimeField(auto_now=True)
    status = IntegerField(
        blank=True,
        default=constants.BASE_ESCRITO_DRAFT,
        choices=constants.BASE_ESCRITO_STATUS,
    )
    # thumbnail = CloudinaryField('image', null=True, width_field='image_width', height_field='image_height')
    thumbnail = ImageField(
        "image",
        blank=True,
        null=True,
        width_field="image_width",
        height_field="image_height",
    )
    non_thumbnail_url = CharField(max_length=500, null=True, blank=True)
    in_text_image = BooleanField(default=False)
    meta_information = ForeignKey(
        "seo.MetaParametersHistorial",
        on_delete=SET_NULL,
        blank=True,
        null=True,
    )

    class Meta:
        abstract = True

    @property
    def current_status(self):
        return constants.ESCRITO_STATUS_MAP[self.status]

    @property
    def image(self):
        return (
            self.thumbnail.url if self.thumbnail else self.non_thumbnail_url
        ) or "/static/general/assets/img/general/why-us.webp"
