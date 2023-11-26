from django.contrib.auth import get_user_model
from django.db.models import CharField

from src.general.abstracts import AbstractTimeStampedModel

User = get_user_model()


class Country(AbstractTimeStampedModel):
    country = CharField(
        max_length=500,
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
    iso = CharField(
        max_length=500,
        default="",
        blank=True,
    )

    alpha_2_code = CharField(
        max_length=2,
        default="",
        blank=True,
    )
    alpha_3_code = CharField(
        max_length=3,
        default="",
        blank=True,
    )

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"
        db_table = "assets_countries"

    def __str__(self):
        return self.country or str(self.pk)
