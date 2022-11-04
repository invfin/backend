from django.contrib.auth import get_user_model
from django.db.models import (
    CharField,
    IntegerField,
    ManyToManyField,
)

from apps.general.abstracts import AbstractTimeStampedModel
from apps.currencies.managers import CurrencyManager
from apps.countries.models import Country

User = get_user_model()


class Currency(AbstractTimeStampedModel):
    created_at = None
    updated_at = None
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
