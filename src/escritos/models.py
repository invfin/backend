from typing import Dict
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import (
    CASCADE,
    SET_NULL,
    BooleanField,
    CharField,
    DateTimeField,
    ForeignKey,
    ManyToManyField,
    Model,
    OneToOneField,
    PositiveIntegerField,
)
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils import timezone

from ckeditor.fields import RichTextField

from .abstracts import AbstractPublishableContent
from src.general.abstracts import AbstractComment, AbstractFavoritesHistorial
from src.general.mixins import BaseToAllMixin

from .managers import TermManager

DOMAIN = settings.FULL_DOMAIN
User = get_user_model()


class Term(AbstractPublishableContent):
    upvotes = ManyToManyField(User, blank=True, related_name="user_upvote_term")
    downvotes = ManyToManyField(User, blank=True, related_name="user_downvote_term")
    meta_information = None
    # contributors = ManyToManyField(User, blank=True, related_name="contributors")
    objects = TermManager()

    class Meta:
        verbose_name = "Término del glosario"
        db_table = "term"
        ordering = ["id"]

    def get_absolute_url(self):
        return reverse("escritos:single_term", kwargs={"slug": self.slug})

    @property
    def term_parts(self):
        return self.term_content_parts.all()

    def link(self):
        return f"{DOMAIN}{self.get_absolute_url()}"

    @property
    def editable_link(self):
        url = reverse("web:manage_single_term", kwargs={"slug": self.slug})
        return f"{DOMAIN}{url}"


class TermContent(Model, BaseToAllMixin):
    term_related = ForeignKey("escritos.Term", on_delete=SET_NULL, null=True, related_name="term_content_parts")
    title = CharField(max_length=3000)
    order = PositiveIntegerField(default=0)
    content = RichTextField()

    class Meta:
        ordering = ["order"]
        verbose_name = "Partes del término"
        db_table = "term_content"

    def __str__(self):
        return f"{self.title}"

    def get_absolute_url(self):
        path = self.term_related.get_absolute_url()
        return f"{path}#{slugify(self.title)}"

    def link(self):
        return f"{DOMAIN}{self.get_absolute_url()}"


class TermCorrection(Model, BaseToAllMixin):
    term_content_related = ForeignKey("escritos.TermContent", null=True, blank=True, on_delete=SET_NULL)
    title = CharField(max_length=3000, blank=True, default="")
    date_suggested = DateTimeField(default=timezone.now)
    is_approved = BooleanField(default=False)
    date_approved = DateTimeField(blank=True, null=True)
    content = RichTextField(config_name="writer", default="")
    original_title = CharField(max_length=3000, default="")
    original_content = RichTextField(config_name="writer", default="")
    reviwed_by = ForeignKey(User, null=True, blank=True, related_name="corrector", on_delete=SET_NULL)
    approved_by = ForeignKey(User, null=True, blank=True, related_name="revisor", on_delete=SET_NULL)

    class Meta:
        ordering = ["id"]
        verbose_name = "Corrections terms"
        db_table = "term_content_correction"

    def __str__(self):
        return f"{self.term_content_related} corregido por {self.reviwed_by}"

    def save(self, *args, **kwargs):
        self.populate_original()
        """
        TODO
        enviar email de agradecimiento
        Perfil.ADD_CREDITS(self.user, 5)
        """
        return super().save(*args, **kwargs)

    def populate_original(self) -> None:
        if not self.id:
            self.original_title = self.term_content_related.title
            self.original_content = self.term_content_related.content

    def get_absolute_url(self):
        return self.term_content_related.get_absolute_url()


class TermsComment(AbstractComment):
    content_related = ForeignKey("escritos.Term", on_delete=CASCADE, null=True, related_name="comments_related")

    class Meta:
        verbose_name = "Term's comment"
        db_table = "term_comments"


class TermsRelatedToResume(Model):
    term_to_keep = ForeignKey("escritos.Term", on_delete=CASCADE, null=True, related_name="term_to_keep")

    term_to_delete = ForeignKey("escritos.Term", on_delete=CASCADE, null=True, related_name="term_to_delete")

    class Meta:
        verbose_name = "Terms to resume"
        db_table = "terms_to_resume"


class FavoritesTermsHistorial(AbstractFavoritesHistorial):
    term = ForeignKey("escritos.Term", on_delete=SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = "Término favorito"
        verbose_name_plural = "Términos favoritos"
        db_table = "favorites_terms_historial"

    def __str__(self):
        return f"{self.user.username}"


class FavoritesTermsList(Model):
    user = OneToOneField(User, on_delete=SET_NULL, null=True, blank=True, related_name="favorites_terms")
    term = ManyToManyField("escritos.Term", blank=True)

    class Meta:
        verbose_name = "Lista de términos favoritos"
        verbose_name_plural = "Lista de términos favoritos"
        db_table = "favorites_terms_list"

    def __str__(self):
        return self.user.username
