import pytest

from django.test import TestCase 

pytestmark = pytest.mark.django_db
from apps.seo.models import Visiteur
from apps.seo.outils.visiteur_meta import SeoInformation


class TestUtils(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
