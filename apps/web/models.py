from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models import (
    SET_NULL,
    BooleanField,
    CharField,
    DateTimeField,
    ForeignKey,
    ManyToManyField,
    PositiveBigIntegerField,
    SlugField,
    TextField,
    Model,
    CASCADE,
)
from django.urls import reverse

from ckeditor.fields import RichTextField

from apps.general.mixins import BaseToAllMixin
from apps.general.bases import BaseTrackEmail, BaseEmail
from apps.seo.models import Visiteur
from apps.socialmedias.constants import SOCIAL_MEDIAS
from apps.seo import constants as seo_constants
from apps.users.models import User
from apps.web import constants


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


class Campaign(Model, BaseToAllMixin):
    title = CharField(max_length=600, blank=True)
    slug = SlugField(max_length=800, null=True, blank=True)
    description = TextField(blank=True)
    categories = ManyToManyField("general.Category", blank=True)
    tags = ManyToManyField("general.Tag", blank=True)
    start_date = DateTimeField(blank=True, null=True)
    end_date = DateTimeField(blank=True, null=True)
    focused_on = CharField(max_length=250, choices=constants.CORE_CAMPAIGN_FOCUS)
    users = ForeignKey("users.UsersCategory", on_delete=CASCADE, null=True, blank=True, related_name="campaigns",)

    class Meta:
        verbose_name = "Campaign"
        db_table = "campaigns"

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.save_unique_field("slug", self.title)
        return super().save(*args, **kwargs)

    @property
    def is_permanent(self) -> bool:
        return not self.end_date


class Promotion(Model, BaseToAllMixin):
    title = CharField(max_length=600, blank=True)
    content = RichTextField()
    thumbnail = CharField(max_length=600, blank=True)
    slug = SlugField(max_length=800, null=True, blank=True)
    prize = PositiveBigIntegerField(default=0)
    shareable_url = SlugField(max_length=600, blank=True)
    redirect_to = SlugField(max_length=600, blank=True)
    medium = CharField(max_length=250, choices=seo_constants.MEDIUMS, default=seo_constants.WEB,)
    web_promotion_style = CharField(max_length=250, choices=seo_constants.WEP_PROMOTION_STYLE, blank=True,)
    web_location = CharField(max_length=250, choices=seo_constants.WEP_PROMOTION_LOCATION, blank=True,)
    web_place = CharField(max_length=250, choices=seo_constants.WEP_PROMOTION_PLACE,blank=True,)
    social_media = CharField(max_length=250, choices=SOCIAL_MEDIAS, blank=True,)
    publication_date = DateTimeField(blank=True)
    campaign = ForeignKey(
        Campaign,
        on_delete=SET_NULL,
        null=True,
        blank=True,
        related_name="promotions",
    )
    reuse = BooleanField(default=False)
    times_to_reuse = PositiveBigIntegerField(default=0)
    users_clicked = ManyToManyField(User, blank=True)
    visiteurs_clicked = ManyToManyField(Visiteur, blank=True)
    clicks_by_user = PositiveBigIntegerField(default=0)
    clicks_by_not_user = PositiveBigIntegerField(default=0)

    class Meta:
        verbose_name = "Promotion"
        db_table = "promotions"

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.save_unique_field("slug", self.title)
        return super().save(*args, **kwargs)

    @property
    def has_prize(self):
        return self.prize != 0

    @property
    def full_url(self):
        source = "web"
        if self.medium != source:
            source = self.social_media
        utm_source = f"utm_source={source}"
        utm_medium = f"&utm_medium={self.medium}"
        utm_campaign = f"&utm_campaign={self.campaign.title}" if self.campaign else ""
        utm_term = f"&utm_term={self.title}"
        return f"{self.redirect_to}?{utm_source}{utm_medium}{utm_campaign}{utm_term}"


class WebsiteEmail(BaseEmail):
    content = RichTextField()
    whom_to_send = CharField(
        max_length=800,
        choices=constants.WHOM_TO_SEND_EMAIL,
        default=constants.WHOM_TO_SEND_EMAIL_ALL,
    )
    campaign = ForeignKey(
        Campaign,
        on_delete=SET_NULL,
        null=True,
        blank=True,
        related_name="emails",
    )
    users_selected = ManyToManyField(User, blank=True)
    content_type = ForeignKey(ContentType, on_delete=CASCADE, null=True)
    object_id = PositiveBigIntegerField(null=True)
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


class WebsiteEmailTrack(BaseTrackEmail):
    email_related = ForeignKey(
        WebsiteEmail,
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
