from django.contrib.auth import get_user_model
from django.db.models import (
    CASCADE,
    SET_NULL,
    BooleanField,
    CharField,
    ForeignKey,
    IntegerField,
    ManyToManyField,
    Model,
)

from cloudinary.models import CloudinaryField

from apps.general import constants
from apps.general.bases import BaseGenericModels, BaseToAllMixin, BaseTrackEmail
from apps.general.managers import CurrencyManager, PeriodManager


User = get_user_model()


class Campaign(Model, BaseToAllMixin):
    title = CharField(max_length=600, blank=True)
    slug = SlugField(max_length=800, null=True, blank=True)
    description = TextField(blank=True)
    categories = ManyToManyField("general.Category", blank=True)
    tags = ManyToManyField("general.Tag", blank=True)
    start_date = DateTimeField(blank=True, null=True)
    end_date = DateTimeField(blank=True, null=True)
    focused_on = CharField(
        max_length=250,
        choices=constants.CORE_CAMPAIGN_FOCUS,
    )
    users_category = ForeignKey(
        "users.UsersCategory",
        on_delete=CASCADE,
        null=True,
        blank=True,
        related_name="campaigns",
    )

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
    medium = CharField(
        max_length=250,
        choices=seo_constants.MEDIUMS,
        default=seo_constants.WEB,
    )
    web_promotion_style = CharField(
        max_length=250,
        choices=seo_constants.WEP_PROMOTION_STYLE,
        blank=True,
    )
    web_location = CharField(
        max_length=250,
        choices=seo_constants.WEP_PROMOTION_LOCATION,
        blank=True,
    )
    web_place = CharField(
        max_length=250,
        choices=seo_constants.WEP_PROMOTION_PLACE,
        blank=True,
    )
    social_media = CharField(
        max_length=250,
        choices=SOCIAL_MEDIAS,
        blank=True,
    )
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
