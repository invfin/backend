from unittest import skip

from django.test import TestCase

from freezegun import freeze_time
import vcr

from src.business import constants
from src.business.models import Product, ProductComplementary, ProductComplementaryPaymentLink
from src.currencies.models import Currency

business_vcr = vcr.VCR(
    cassette_library_dir="cassettes/business/",
    path_transformer=vcr.VCR.ensure_suffix(".yaml"),
)


@skip("Need to be better")
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
            payment_type=constants.TYPE_ONE_TIME,
        )

    @business_vcr.use_cassette
    @freeze_time("2022-04-01")
    def test_product_pre_save(self):
        first_prod = Product.objects.create(for_testing=True, title="New prod")
        first_prod.refresh_from_db()
        assert "New prod" == first_prod.description
        assert "new-prod" == first_prod.slug
        # assert("new-prod", first_prod.stripe_id)

    @business_vcr.use_cassette
    def test_product_complementary_pre_save(self):
        prod_comp_subs = ProductComplementary.objects.create(
            product=self.base_prod,
            title="Subscription prod complementary",
            price=54.45,
            currency=self.currency,
            payment_type=constants.TYPE_SUBSCRIPTION,
            subscription_period=constants.PERIOD_MONTHLY,
            subscription_interval=2,
        )
        prod_comp_subs.refresh_from_db()
        assert "Subscription prod complementary" == prod_comp_subs.description
        assert "subscription-prod-complementary" == prod_comp_subs.slug
        assert self.base_prod.for_testing == prod_comp_subs.for_testing
        assert prod_comp_subs.for_testing is True
        # assert("new-prod", prod_comp_subs.stripe_id)

        prod_comp_pay = ProductComplementary.objects.create(
            product=self.base_prod,
            title="Payment prod complementary",
            price=23.45,
            currency=self.currency,
            payment_type=constants.TYPE_ONE_TIME,
        )
        prod_comp_pay.refresh_from_db()
        assert "Payment prod complementary" == prod_comp_pay.description
        assert "payment-prod-complementary" == prod_comp_pay.slug
        assert self.base_prod.for_testing == prod_comp_pay.for_testing
        assert prod_comp_pay.for_testing is True
        # assert("new-prod" == prod_comp_pay.stripe_id)

    @business_vcr.use_cassette
    def test_complementary_payment_link_pre_save(self):
        prod_com_link = ProductComplementaryPaymentLink.objects.create(
            product_complementary=self.base_prod_comp,
            title="Prod payment link",
            for_website=True,
        )
        prod_com_link.refresh_from_db()
        assert "self.base_prod.for_testing" == prod_com_link.link
        assert "self.base_prod.for_testing" == prod_com_link.stripe_id
