import vcr
from model_bakery import baker

from django.test import TestCase

from apps.public_blog.models import (
EmailPublicBlog,
FollowingHistorial,
NewsletterFollowers,
PublicBlog,
PublicBlogAsNewsletter,
PublicBlogComment,
WritterProfile,
)

public_blog_vcr = vcr.VCR(
    cassette_library_dir='cassettes/public_blog/models/',
    path_transformer=vcr.VCR.ensure_suffix('.yaml'),
)


class TestEmailPublicBlog(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestFollowingHistorial(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestNewsletterFollowers(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestPublicBlog(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test_get_absolute_url(self):
        pass
    

class TestPublicBlogAsNewsletter(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestPublicBlogComment(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestWritterProfile(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
