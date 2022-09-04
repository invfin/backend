from django.test import TestCase

from apps.seo.models import Visiteur
from apps.seo.outils.visiteur_meta import SeoInformation
from apps.seo.tasks import clean_journeys, loop_over_journeys

class TestTasks(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def test_clean_journeys(self):
        for user_journey_model in ['User', 'Visiteur']:
            clean_journeys()

    def test_loop_over_journeys(self):
        pass

