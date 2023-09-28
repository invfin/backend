from django.db.models import (
    CASCADE,
    SET_NULL,
    CharField,
    ForeignKey,
    IntegerField,
    ManyToManyField,
    OneToOneField,
)

from src.countries.models import Country
from src.currencies.managers import CurrencyManager
from src.general.abstracts import AbstractTimeStampedModel
from src.users.models import User


class Currency(AbstractTimeStampedModel):
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
        return self.currency


class UserDefaultCurrency(AbstractTimeStampedModel):
    user = OneToOneField(
        User,
        on_delete=CASCADE,
    )
    currency = ForeignKey(
        Currency,
        on_delete=SET_NULL,
        null=True,
        blank=True,
        default="1",
    )

    class Meta:
        db_table = "assets_user_default_currencies"

    def __str__(self):
        return self.currency
