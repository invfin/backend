from unittest import skip

from django.test import TestCase

from src.seo.tasks import clean_journeys


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
