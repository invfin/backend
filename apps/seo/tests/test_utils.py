import pytest

from apps.seo.models import Visiteur
from apps.seo.outils.visiteur_meta import SeoInformation

pytestmark = pytest.mark.django_db


class TestUtils:
    @classmethod
    def setup_class(cls):
        pass
