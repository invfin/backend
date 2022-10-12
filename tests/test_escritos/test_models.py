import pytest

from bfet import DjangoTestingModel

from django.conf import settings

from django.template.defaultfilters import slugify

from apps.escritos.models import (
    FavoritesTermsHistorial,
    FavoritesTermsList,
    Term,
    TermContent,
    TermCorrection,
    TermsComment,
    TermsRelatedToResume,
)


FULL_DOMAIN = settings.FULL_DOMAIN


from django.test import TestCase


class TestTerm(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.term = DjangoTestingModel.create(Term, title="test contenido", slug="test-contenido")

    def test_link(self):
        assert f"{FULL_DOMAIN}/definicion/test-contenido/" == self.term.link()


from django.test import TestCase


class TestTermContent(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.term_contet = DjangoTestingModel.create(
            TermContent,
            title="test contenido",
            term_related=DjangoTestingModel.create(Term, slug="test-main-contenido"),
        )

    def test_get_absolute_url(self):
        slug = "test-contenido"
        path = "/definicion/test-main-contenido/"
        assert f"{path}#{slug}" == self.term_contet.get_absolute_url()

    def test_link(self):
        slug = "test-contenido"
        path = "/definicion/test-main-contenido/"
        assert f"{FULL_DOMAIN}{path}#{slug}" == self.term_contet.link()
