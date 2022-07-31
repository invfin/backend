import vcr
from model_bakery import baker

from django.test import TestCase

from apps.seo.mixins import (
SEOViewMixin,
)

seo_vcr = vcr.VCR(
    cassette_library_dir='cassettes/seo/mixins/',
    path_transformer=vcr.VCR.ensure_suffix('.yaml'),
)


class TestSEOViewMixin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test_get_base_meta_information(self):
        pass
    
    def test_get_context_data(self):
        pass
    
    def test_get_meta_author(self):
        pass
    
    def test_get_meta_category(self):
        pass
    
    def test_get_meta_description(self):
        pass
    
    def test_get_meta_image(self):
        pass
    
    def test_get_meta_information(self):
        pass
    
    def test_get_meta_modified_time(self):
        pass
    
    def test_get_meta_published_time(self):
        pass
    
    def test_get_meta_tags(self):
        pass
    
    def test_get_meta_title(self):
        pass
    
    def test_get_meta_twitter_author(self):
        pass
    
    def test_get_meta_url(self):
        pass
    
    def test_get_open_graph_type(self):
        pass
    
    def test_get_possible_meta_attribute(self):
        pass
    
    def test_get_schema_org(self):
        pass
    
    def test_update_views(self):
        pass
    
