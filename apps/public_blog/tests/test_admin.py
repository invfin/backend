import vcr
from model_bakery import baker

from django.test import TestCase

from apps.public_blog.admin import (
FollowingHistorialAdmin,
NewsletterFollowersAdmin,
NewsletterInline,
PublicBlogAdmin,
PublicBlogAsNewsletterAdmin,
PublicBlogCommentAdmin,
WritterProfileAdmin,
)

public_blog_vcr = vcr.VCR(
    cassette_library_dir='cassettes/public_blog/admin/',
    path_transformer=vcr.VCR.ensure_suffix('.yaml'),
)


class TestFollowingHistorialAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestNewsletterFollowersAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestNewsletterInline(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestPublicBlogAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestPublicBlogAsNewsletterAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestPublicBlogCommentAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestWritterProfileAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
