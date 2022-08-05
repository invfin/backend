import vcr

from freezegun import freeze_time

from django.test import TestCase

from apps.business.models import (
    Product,
    ProductComplementary,
    ProductComplementaryPaymentLink,
)
from apps.business import constants
from apps.general.models import Currency

business_vcr = vcr.VCR(
    cassette_library_dir='cassettes/business/',
    path_transformer=vcr.VCR.ensure_suffix('.yaml'),
)


class TestBusinessSignal(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.currency = Currency.objects.create(
            currency="eur",
            symbol="€",
            name="Euro",
            iso="",
            decimals="2",
        )
        cls.base_prod = Product.objects.create(
            for_testing=True,
            title="Base prod",
            slug="base-prod",
            description="Base prod",
        )
        cls.base_prod_comp = ProductComplementary.objects.create(
            product=cls.base_prod,
            title="Base payment prod complementary",
            price=23.45,
            currency=cls.currency,
            payment_type=constants.TYPE_ONE_TIME
        )

    @business_vcr
    @freeze_time("2022-04-01")
    def test_product_pre_save(self):
        first_prod = Product.objects.create(
            for_testing=True,
            title="New prod"
        )
        first_prod.refresh_from_db()
        self.asserEqual("New prod", first_prod.description)
        self.asserEqual("new-prod", first_prod.slug)
        # self.asserEqual("new-prod", first_prod.stripe_id)

    @business_vcr
    def test_product_complementary_pre_save(self):
        prod_comp_subs = ProductComplementary.objects.create(
            product=self.base_prod,
            title="Subscription prod complementary",
            price=54.45,
            currency=self.currency,
            payment_type=constants.TYPE_SUBSCRIPTION,
            subscription_period=constants.PERIOD_MONTHLY,
            subscription_interval=2
        )
        prod_comp_subs.refresh_from_db()
        self.asserEqual(
            "Subscription prod complementary",
            prod_comp_subs.description
        )
        self.asserEqual(
            "subscription-prod-complementary",
            prod_comp_subs.slug
        )
        self.asserEqual(
            self.base_prod.for_testing,
            prod_comp_subs.for_testing
        )
        self.asserEqual(
            True,
            prod_comp_subs.for_testing
        )
        # self.asserEqual("new-prod", prod_comp_subs.stripe_id)

        prod_comp_pay = ProductComplementary.objects.create(
            product=self.base_prod,
            title="Payment prod complementary",
            price=23.45,
            currency=self.currency,
            payment_type=constants.TYPE_ONE_TIME
        )
        prod_comp_pay.refresh_from_db()
        self.asserEqual(
            "Payment prod complementary",
            prod_comp_pay.description
        )
        self.asserEqual(
            "payment-prod-complementary",
            prod_comp_pay.slug
        )
        self.asserEqual(
            self.base_prod.for_testing,
            prod_comp_pay.for_testing
        )
        self.asserEqual(
            True,
            prod_comp_pay.for_testing
        )
        # self.asserEqual("new-prod", prod_comp_pay.stripe_id)

    @business_vcr
    def test_complementary_payment_link_pre_save(self):
        prod_com_link = ProductComplementaryPaymentLink.objects.create(
            product_complementary=self.base_prod_comp,
            title="Prod payment link",
            for_website=True,
        )
        prod_com_link.refresh_from_db()
        self.asserEqual(
            "self.base_prod.for_testing",
            prod_com_link.link
        )
        self.asserEqual(
            "self.base_prod.for_testing",
            prod_com_link.stripe_id
        )
