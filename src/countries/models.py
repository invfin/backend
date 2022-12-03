from django.contrib.auth import get_user_model
from django.db.models import CharField

from src.general.abstracts import AbstractTimeStampedModel

User = get_user_model()


class Country(AbstractTimeStampedModel):
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
