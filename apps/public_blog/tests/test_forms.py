import vcr
from model_bakery import baker

from django.test import TestCase

from apps.public_blog.forms import (
PublicBlogForm,
WritterProfileForm,
)

public_blog_vcr = vcr.VCR(
    cassette_library_dir='cassettes/public_blog/forms/',
    path_transformer=vcr.VCR.ensure_suffix('.yaml'),
)


class TestPublicBlogForm(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestWritterProfileForm(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
