from django.contrib.auth import get_user_model
from django.db.models import (
    CharField,
    Model
)

from apps.general.mixins import BaseToAllMixin


User = get_user_model()


class AbstractClassification(Model, BaseToAllMixin):
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


class Category(AbstractClassification):
    class Meta:
        verbose_name = "Category"
        db_table = "categories"


class Tag(AbstractClassification):
    class Meta:
        verbose_name = "Tag"
        db_table = "tags"
