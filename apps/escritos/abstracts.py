from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericRelation
from django.db.models import (
    SET_NULL,
    BooleanField,
    CharField,
    DateTimeField,
    ForeignKey,
    ManyToManyField,
    IntegerField,
    PositiveIntegerField,
    JSONField,
    TextField,
    ImageField,
)

from apps.general.abstracts import AbstractTimeStampedModel
from apps.general.mixins import CommentsMixin, VotesMixin
from apps.classifications.models import Tag
from apps.escritos import constants

User = get_user_model()

class AbstractWrittenContent(AbstractTimeStampedModel, CommentsMixin, VotesMixin):
    title = CharField(max_length=500, null=True, blank=True)
    slug = CharField(max_length=500, null=True, blank=True)  # TODO change to slug field and allow blank but not null
    total_votes = IntegerField(default=0)
    total_views = PositiveIntegerField(default=0)
    times_shared = PositiveIntegerField(default=0)
    category = ForeignKey(
        "general.Category",
        on_delete=SET_NULL,
        blank=True,
        null=True,
    )
    tags = ManyToManyField("general.Tag", blank=True)
    author = ForeignKey(User, on_delete=SET_NULL, null=True)
    checkings = JSONField(default=default_dict)
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

    def add_tags(self, tags):
        for tag in tags:
            if tag == "":
                continue
            tag, created = Tag.objects.get_or_create(slug=tag.lower())
            if tag in self.tags.all():
                continue
            self.tags.add(tag)


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
        image = self.non_thumbnail_url
        if self.thumbnail:
            image = self.thumbnail.url
        if not image:
            image = "/static/general/assets/img/general/why-us.webp"
        return image
