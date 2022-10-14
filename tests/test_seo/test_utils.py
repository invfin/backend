import pytest

from apps.seo.models import Visiteur
from apps.seo.outils.visiteur_meta import SeoInformation


from django.test import TestCase


class TestUtils(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
