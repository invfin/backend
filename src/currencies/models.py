from decimal import Decimal

from django.db.models import (
    CASCADE,
    SET_NULL,
    CharField,
    DateField,
    DecimalField,
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
        default="",
        blank=True,
    )
    symbol = CharField(
        max_length=5,
        default="",
        blank=True,
    )
    name = CharField(
        max_length=500,
        default="",
        blank=True,
    )
    spanish_name = CharField(
        max_length=500,
        default="",
        blank=True,
    )
    code = CharField(
        max_length=10,
        default="",
        blank=True,
    )
    iso = CharField(
        max_length=500,
        blank=True,
        default="",
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
        return self.code or self.currency


class ExchangeRate(AbstractTimeStampedModel):
    base = ForeignKey(Currency, on_delete=CASCADE, related_name="rates_from")  # From
    target = ForeignKey(Currency, on_delete=CASCADE, related_name="rates_to")  # To
    conversion_rate = DecimalField(max_digits=100, decimal_places=3, default=Decimal(0.0))
    date = DateField()

    class Meta:
        unique_together = [["base", "target", "date"]]
        db_table = "assets_exchange_rate"
        ordering = ["created_at"]

    def __str__(self):
        return (
            f"{self.base.code}: 1 - "
            f"{self.target.code}: {self.conversion_rate:.4f} - {self.date}"
        )


class UserDefaultCurrency(AbstractTimeStampedModel):
    user = OneToOneField(User, on_delete=CASCADE, related_name="currency")
    currency = ForeignKey(
        Currency,
        on_delete=SET_NULL,
        null=True,
        blank=True,
        default="1",  # type: ignore
    )  # type: ignore

    class Meta:
        db_table = "assets_user_default_currencies"

    def __str__(self):
        return self.currency.symbol
