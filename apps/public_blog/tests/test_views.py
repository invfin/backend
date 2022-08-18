import vcr
from model_bakery import baker

from django.test import TestCase

from apps.public_blog.views import (
CreatePublicBlogPostView,
PublicBlogDetailsView,
PublicBlogsListView,
UpdateBlogNewsletterView,
UpdatePublicBlogPostView,
WritterOnlyView,
WritterOwnBlogsListView,
)

public_blog_vcr = vcr.VCR(
    cassette_library_dir='cassettes/public_blog/views/',
    path_transformer=vcr.VCR.ensure_suffix('.yaml'),
)


class TestCreatePublicBlogPostView(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test_form_valid(self):
        pass
    
    def test_get_context_data(self):
        pass
    

class TestPublicBlogDetailsView(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test_get_context_data(self):
        pass
    

class TestPublicBlogsListView(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test_get_context_data(self):
        pass
    
    def test_get_queryset(self):
        pass
    

class TestUpdateBlogNewsletterView(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test_get_context_data(self):
        pass
    
    def test_test_func(self):
        pass
    

class TestUpdatePublicBlogPostView(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test_form_valid(self):
        pass
    
    def test_get_context_data(self):
        pass
    
    def test_get_success_url(self):
        pass
    
    def test_test_func(self):
        pass
    

class TestWritterOnlyView(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test_handle_no_permission(self):
        pass
    
    def test_test_func(self):
        pass
    

class TestWritterOwnBlogsListView(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test_get_context_data(self):
        pass
    
