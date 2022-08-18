import vcr
from model_bakery import baker

from django.test import TestCase

from apps.business.admin import (
BaseStripeAdmin,
CustomerAdmin,
ProductAdmin,
ProductCommentAdmin,
ProductComplementaryAdmin,
ProductComplementaryInline,
ProductComplementaryPaymentLinkInline,
ProductDiscountAdmin,
StripeWebhookResponseAdmin,
TransactionHistorialAdmin,
)

business_vcr = vcr.VCR(
    cassette_library_dir='cassettes/business/admin/',
    path_transformer=vcr.VCR.ensure_suffix('.yaml'),
)


class TestBaseStripeAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestCustomerAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestProductAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestProductCommentAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestProductComplementaryAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestProductComplementaryInline(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestProductComplementaryPaymentLinkInline(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestProductDiscountAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestStripeWebhookResponseAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestTransactionHistorialAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
