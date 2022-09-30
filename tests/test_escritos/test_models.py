import pytest

from bfet import DjangoTestingModel as DTM

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

pytestmark = pytest.mark.django_db
FULL_DOMAIN = settings.FULL_DOMAIN


@pytest.mark.django_db
class TestTerm:
    @classmethod
    def setup_class(cls):
        cls.term = DTM.create(Term, title="test contenido", slug="test-contenido")

    def test_link(self):
        assert f"{FULL_DOMAIN}/definicion/test-contenido/" == self.term.link()


@pytest.mark.django_db
class TestTermContent:
    @classmethod
    def setup_class(cls):
        cls.term_contet = DTM.create(
            TermContent, title="test contenido", term_related=DTM.create(Term, slug="test-main-contenido")
        )

    def test_get_absolute_url(self):
        slug = "test-contenido"
        path = "/definicion/test-main-contenido/"
        assert f"{path}#{slug}" == self.term_contet.get_absolute_url()

    def test_link(self):
        slug = "test-contenido"
        path = "/definicion/test-main-contenido/"
        assert f"{FULL_DOMAIN}{path}#{slug}" == self.term_contet.link()
