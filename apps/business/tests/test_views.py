import vcr
from model_bakery import baker

from django.test import TestCase

from apps.business.views import (
CheckoutRedirectView,
CreateCheckoutView,
CreateUserFromCustomerRecentPurchase,
ProductDetailView,
ProductsListView,
)

business_vcr = vcr.VCR(
    cassette_library_dir='cassettes/business/views/',
    path_transformer=vcr.VCR.ensure_suffix('.yaml'),
)


class TestCheckoutRedirectView(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test_get(self):
        pass
    
    def test_save_transaction(self):
        pass
    

class TestCreateCheckoutView(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test_get(self):
        pass
    

class TestCreateUserFromCustomerRecentPurchase(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test_get(self):
        pass
    

class TestProductDetailView(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test_get(self):
        pass
    
    def test_get_object(self):
        pass
    

class TestProductsListView(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test_get_queryset(self):
        pass
    
