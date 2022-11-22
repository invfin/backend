from unittest import skip

from apps.seo.models import Visiteur
from apps.seo.outils.visiteur_meta import SeoInformation
from apps.seo.tasks import clean_journeys, loop_over_journeys


from django.test import TestCase


class TestTasks(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    @skip("not ready")
    def test_clean_journeys(self):
        for user_journey_model in ["User", "Visiteur"]:
            clean_journeys()

    @skip("not ready")
    def test_loop_over_journeys(self):
        pass
