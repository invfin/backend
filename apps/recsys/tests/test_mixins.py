import vcr
from model_bakery import baker

from django.test import TestCase

from apps.recsys.mixins import (
RecommenderMixin,
)

recsys_vcr = vcr.VCR(
    cassette_library_dir='cassettes/recsys/mixins/',
    path_transformer=vcr.VCR.ensure_suffix('.yaml'),
)


class TestRecommenderMixin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test_generate_recsys_path(self):
        pass
    
    def test_get_context_data(self):
        pass
    
