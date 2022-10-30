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


class EscritosClassification(Model, BaseToAllMixin):
    name = CharField(
        max_length=500,
        null=True,
        blank=True,
        unique=True,
    )
    slug = CharField(
        max_length=500,
        null=True,
        blank=True,
        unique=True,
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name or f"{self.pk}"

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = self.save_unique_field("slug", self.name)
        return super().save(*args, **kwargs)


class Category(EscritosClassification):
    class Meta:
        verbose_name = "Category"
        db_table = "categories"


class Tag(EscritosClassification):
    class Meta:
        verbose_name = "Tag"
        db_table = "tags"


class Industry(Model):
    industry = CharField(
        max_length=500,
        null=True,
        blank=True,
    )
    industry_spanish = CharField(
        max_length=500,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Industry"
        verbose_name_plural = "Industries"
        db_table = "assets_industries"

    def __str__(self):
        return str(self.industry)


class Sector(Model):
    sector = CharField(
        max_length=500,
        null=True,
        blank=True,
    )
    sector_spanish = CharField(
        max_length=500,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Sector"
        verbose_name_plural = "Sectors"
        db_table = "assets_sectors"

    def __str__(self):
        return str(self.sector)


class Country(Model):
    country = CharField(
        max_length=500,
        null=True,
        blank=True,
    )
    name = CharField(
        max_length=500,
        null=True,
        blank=True,
    )
    spanish_name = CharField(
        max_length=500,
        null=True,
        blank=True,
    )
    iso = CharField(
        max_length=500,
        null=True,
        blank=True,
    )

    alpha_2_code = CharField(
        max_length=2,
        null=True,
        blank=True,
    )
    alpha_3_code = CharField(
        max_length=3,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"
        db_table = "assets_countries"

    def __str__(self):
        return str(self.country)


class Currency(Model):
    currency = CharField(
        max_length=500,
        null=True,
        blank=True,
    )
    symbol = CharField(
        max_length=5,
        null=True,
        blank=True,
    )
    name = CharField(
        max_length=500,
        null=True,
        blank=True,
    )
    spanish_name = CharField(
        max_length=500,
        null=True,
        blank=True,
    )
    accronym = CharField(
        max_length=10,
        null=True,
        blank=True,
    )
    iso = CharField(
        max_length=500,
        null=True,
        blank=True,
    )
    decimals = IntegerField(
        default=2,
        blank=True,
    )
    countries = ManyToManyField(
        Country,
        blank=True,
        related_name="currency",
    )
    objects = CurrencyManager()

    class Meta:
        verbose_name = "Currency"
        verbose_name_plural = "Currencies"
        db_table = "assets_currencies"

    def __str__(self):
        return str(self.currency)


class Notification(BaseGenericModels):
    user = ForeignKey(User, on_delete=CASCADE)
    notification_type = CharField(max_length=500, choices=constants.NOTIFICATIONS_TYPE)
    is_seen = BooleanField(default=False)

    class Meta:
        verbose_name = "Notification"
        db_table = "notifications"


class EmailNotification(BaseTrackEmail):
    email_related = ForeignKey(Notification, null=True, blank=True, on_delete=SET_NULL, related_name="email_related")

    class Meta:
        verbose_name = "Email from notifications"
        db_table = "emails_notifications"


class Period(Model):
    year = IntegerField(null=True, blank=True)
    period = IntegerField(choices=constants.PERIODS, null=True, blank=True)
    objects = PeriodManager()

    class Meta:
        verbose_name = "Period"
        verbose_name_plural = "Periods"
        db_table = "assets_periods"
        ordering = ["-year", "-period"]
        get_latest_by = ["-year", "-period"]

    def __str__(self):
        if self.is_full_year:
            return f"FY {str(self.period_year)}"
        return f"Q{self.period} {str(self.period_year)}"

    @property
    def is_full_year(self):
        return self.period == constants.PERIOD_FOR_YEAR

    @property
    def period_year(self):
        return self.year
