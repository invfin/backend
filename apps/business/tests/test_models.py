import vcr
from model_bakery import baker

from django.test import TestCase

from apps.business.models import (
Customer,
Product,
ProductComment,
ProductComplementary,
ProductComplementaryPaymentLink,
ProductDiscount,
ProductSubscriber,
StripeFields,
StripeWebhookResponse,
TransactionHistorial,
)

business_vcr = vcr.VCR(
    cassette_library_dir='cassettes/business/models/',
    path_transformer=vcr.VCR.ensure_suffix('.yaml'),
)


class TestCustomer(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test___str__(self):
        pass
    

class TestProduct(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test___str__(self):
        pass
    
    def test_get_absolute_url(self):
        pass
    

class TestProductComment(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test___str__(self):
        pass
    

class TestProductComplementary(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test___str__(self):
        pass
    

class TestProductComplementaryPaymentLink(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test___str__(self):
        pass
    

class TestProductDiscount(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test___str__(self):
        pass
    

class TestProductSubscriber(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test___str__(self):
        pass
    

class TestStripeFields(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestStripeWebhookResponse(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test___str__(self):
        pass
    

class TestTransactionHistorial(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test___str__(self):
        pass
    
