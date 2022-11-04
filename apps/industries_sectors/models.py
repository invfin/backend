from django.contrib.auth import get_user_model
from django.db.models import (
    CharField,
    Model,
)


User = get_user_model()


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
