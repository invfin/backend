from django.db.models import CharField, Model

from src.general.mixins import BaseToAllMixin

from .managers import TagManager


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
    objects = TagManager()

    class Meta:
        verbose_name = "Tag"
        db_table = "tags"
