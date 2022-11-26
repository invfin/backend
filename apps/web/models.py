from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.db.models import (
    SET_NULL,
    IntegerField,
    CharField,
    ForeignKey,
    ManyToManyField,
    PositiveBigIntegerField,
    SlugField,
    Model,
    CASCADE,
)
from django.urls import reverse

from ckeditor.fields import RichTextField

from apps.general.mixins import BaseToAllMixin, CommentsMixin, VotesMixin
from apps.general.abstracts import AbstractTimeStampedModel, AbstractComment
from apps.emailing.abstracts import AbstractTrackEmail, AbstractEmail
from apps.web import constants
from apps.web.managers import RoadmapManager

User = get_user_model()


class WebsiteLegalPage(Model, BaseToAllMixin):
    title = CharField(max_length=800)
    slug = SlugField(max_length=800, null=True, blank=True)
    content = RichTextField()

    class Meta:
        ordering = ["-id"]
        verbose_name = "Legal website page"
        db_table = "website_pages_legals"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.save_unique_field("slug", self.title)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("web:asuntos_legales", kwargs={"slug": self.slug})


class WebsiteEmail(AbstractEmail):
    content = RichTextField()
    whom_to_send = CharField(
        max_length=800,
        choices=constants.WHOM_TO_SEND_EMAIL,
        default=constants.WHOM_TO_SEND_EMAIL_ALL,
    )
    campaign = ForeignKey(
        "promotions.Campaign",
        on_delete=SET_NULL,
        null=True,
        blank=True,
        related_name="emails",
    )
    users_selected = ManyToManyField(User, blank=True)
    content_type = ForeignKey(ContentType, on_delete=CASCADE, null=True, blank=True)
    object_id = PositiveBigIntegerField(null=True, blank=True)
    object = GenericForeignKey("content_type", "object_id")

    class Meta:
        ordering = ["-id"]
        verbose_name = "Website emails"
        db_table = "website_emails"

    def __str__(self) -> str:
        return self.title

    @property
    def edit_url(self):
        return reverse("web:update_email_engagement", args=[self.pk])

    @property
    def previsualization_url(self):
        return reverse("web:preview_email_engagement", args=[self.pk])

    @property
    def previsualization_template(self):
        template = self.campaign.slug.split("-")[0]
        return f"emailing/web/{template}.html"

    @property
    def status_draft(self):
        return not self.date_to_send

    @property
    def status_sent(self):
        return self.sent

    @property
    def status_waiting(self):
        return self.date_to_send and not self.sent

    @property
    def status(self):
        if not self.date_to_send:
            status = "draft"
            color = "red"
            icon = "minus-circle"
            bs_color = "danger"
        else:
            if self.sent:
                status = "sent"
                color = "green"
                icon = "check-circle"
                bs_color = "success"
            else:
                status = "waiting"
                color = "orange"
                icon = "eye"
                bs_color = "warning"
        return {"status": status, "color": color, "icon": icon, "bs_color": bs_color}


class WebsiteEmailTrack(AbstractTrackEmail):
    email_related = ForeignKey(
        "web.WebsiteEmail",
        null=True,
        blank=True,
        on_delete=SET_NULL,
        related_name="email_related",
    )

    class Meta:
        verbose_name = "Email counting"
        db_table = "website_emails_track"

    def __str__(self) -> str:
        return self.email_related.title


class Roadmap(AbstractTimeStampedModel, CommentsMixin, VotesMixin):
    author = ForeignKey(User, on_delete=SET_NULL, null=True)
    title = CharField(max_length=800)
    slug = SlugField(max_length=800, blank=True)
    content = RichTextField()
    total_votes = IntegerField(default=0)
    total_views = PositiveBigIntegerField(default=0)
    tags = ManyToManyField("classifications.Tag", blank=True)
    status = CharField(max_length=30, choices=constants.ROADMAP_STATUS, default=constants.ROADMAP_STATUS_PENDING)
    upvotes = ManyToManyField(
        User,
        blank=True,
        related_name="user_upvote_roadmap",
    )
    downvotes = ManyToManyField(
        User,
        blank=True,
        related_name="user_downvote_roadmap",
    )
    objects = RoadmapManager()

    class Meta:
        verbose_name = "Roadmap"
        db_table = "website_roadmap"

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.save_unique_field("slug", self.title)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("web:roadmap", kwargs={"slug": self.slug})

    @property
    def icon_color(self):
        return constants.ROADMAP_STATUS_MAP_COLOR_ICON[self.status]

    @property
    def spanish_status(self):
        return constants.ROADMAP_STATUS_MAP[self.status]


class RoadmapComment(AbstractComment):
    content_related = ForeignKey("web.Roadmap", on_delete=CASCADE, null=True, related_name="comments_related")

    class Meta:
        verbose_name = "Roadmap's comment"
        db_table = "website_roadmap_comments"
