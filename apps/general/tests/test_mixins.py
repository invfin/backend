import vcr
from model_bakery import baker

from django.test import TestCase

from apps.general.mixins import (
BaseEscritosMixins,
BaseToAll,
CommonMixin,
ResizeImageMixin,
)

general_vcr = vcr.VCR(
    cassette_library_dir='cassettes/general/mixins/',
    path_transformer=vcr.VCR.ensure_suffix('.yaml'),
)


class TestBaseEscritosMixins(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test_create_meta_information(self):
        pass
    
    def test_extra_info(self):
        pass
    
    def test_save_secondary_info(self):
        pass
    
    def test_search_image(self):
        pass
    

class TestBaseToAll(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test_save_unique_field(self):
        pass
    

class TestCommonMixin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test_vote(self):
        pass
    

class TestResizeImageMixin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test_resize(self):
        pass
    
