import vcr
from model_bakery import baker

from django.test import TestCase

from apps.public_blog.managers import (
PublicBlogManager,
)

public_blog_vcr = vcr.VCR(
    cassette_library_dir='cassettes/public_blog/managers/',
    path_transformer=vcr.VCR.ensure_suffix('.yaml'),
)


class TestPublicBlogManager(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test_get_random(self):
        pass
    
