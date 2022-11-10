from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models import (
    CASCADE,
    SET_NULL,
    BooleanField,
    DateTimeField,
    ForeignKey,
    Model,
    PositiveIntegerField,
    TextField,
)

from apps.general.mixins import BaseToAllMixin


User = get_user_model()


class AbstractTimeStampedModel(Model, BaseToAllMixin):
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class AbstractComment(AbstractTimeStampedModel):
    author = ForeignKey(User, on_delete=SET_NULL, null=True)
    content = TextField()

    class Meta:
        abstract = True

    def get_absolute_url(self):
        return self.content_related.get_absolute_url()

    @property
    def title(self):
        return self.content_related.title


class AbstractGenericModels(AbstractTimeStampedModel):
    content_type = ForeignKey(ContentType, on_delete=CASCADE)
    object_id = PositiveIntegerField()
    object = GenericForeignKey("content_type", "object_id")
    date = DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        if self.object:
            return self.object.get_absolute_url()
        else:
            return reverse("users:user_inicio")


class AbstractFavoritesHistorial(AbstractTimeStampedModel):
    user = ForeignKey(User, on_delete=SET_NULL, null=True, blank=True)
    date = DateTimeField(auto_now_add=True)
    added = BooleanField(default=False)
    removed = BooleanField(default=False)

    class Meta:
        abstract = True
