from model_bakery import baker

from django.conf import settings
from django.test import TestCase
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


class TestTerm(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.term = term = baker.make(
            Term,
            title="test contenido",
            slug="test-contenido"
        )
    
    def test_link(self):
        self.assertEqual(
            f'{FULL_DOMAIN}/definicion/test-contenido/',
            self.term.link()
        )
    

class TestTermContent(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.term_contet = baker.make(
            TermContent,
            title="test contenido",
            term_related=baker.make(
                Term,
                slug="test-main-contenido"
            )
        )
    
    def test_get_absolute_url(self):
        slug = "test-contenido"
        path = "/definicion/test-main-contenido/"
        self.assertEqual(
            f'{path}#{slug}',
            self.term_contet.get_absolute_url()
        )
    
    def test_link(self):
        slug = "test-contenido"
        path = "/definicion/test-main-contenido/"
        self.assertEqual(
            f'{FULL_DOMAIN}{path}#{slug}',
            self.term_contet.link()
        )
