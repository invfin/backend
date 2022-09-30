import pytest

from apps.seo.models import Visiteur
from apps.seo.outils.visiteur_meta import SeoInformation
from apps.seo.tasks import clean_journeys, loop_over_journeys

pytestmark = pytest.mark.django_db


@pytest.mark.django_db
class TestTasks:
    @classmethod
    def setup_class(cls):
        pass

    def test_clean_journeys(self):
        for user_journey_model in ["User", "Visiteur"]:
            clean_journeys()

    def test_loop_over_journeys(self):
        pass
