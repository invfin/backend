from unittest.mock import MagicMock, patch

from django.test import TestCase

from src.business import constants
from src.business.models import Product, ProductComplementary
from src.business.views import CheckoutRedirectView
from src.currencies.models import Currency

EXAMPLE_URL_PARAMS = "prod=10&session_id=cs_test_a1efUTq7VYePHRp07jtfRK5UmIOepUGV1HMgpAjWIfgo7NFHEwgLkZ1OKT"


class TestCheckoutRedirectView(TestCase):
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
        cls.request = MagicMock()
        cls.view = CheckoutRedirectView()
        cls.view.request = cls.request

    @patch("src.business.views.CheckoutRedirectView.handle_messages")
    def test_get(self, mock_handle_messages):
        response = CheckoutRedirectView().get(MagicMock())
        mock_handle_messages.assert_called_once()
        self.assertEqual(response.status_code, 302)

    @patch("src.business.views.CheckoutRedirectView.handle_transaction")
    @patch("django.contrib.messages.success")
    def test_handle_messages_success(
        self,
        mock_success,
        mock_handle_transaction,
    ):
        mock_handle_transaction.return_value = True
        self.view.handle_messages()
        mock_handle_transaction.assert_called_once()
        mock_success.assert_called_once_with(
            self.request,
            "Gracias por tu confianza.",
        )

    @patch("src.business.views.CheckoutRedirectView.handle_transaction")
    @patch("django.contrib.messages.error")
    def test_handle_messages_error(
        self,
        mock_error,
        mock_handle_transaction,
    ):
        mock_handle_transaction.return_value = False
        self.view.handle_messages()
        mock_handle_transaction.assert_called_once()
        mock_error.assert_called_once_with(
            self.request,
            "Lo lamentamos ha sucedido un error. Lo estamos resolviendo",
        )

    @patch("src.business.views.CheckoutRedirectView.get_stripe_info")
    @patch("src.business.views.CheckoutRedirectView.get_customer")
    @patch("src.business.views.CheckoutRedirectView.save_transaction")
    def test_handle_transaction_failed(
        self,
        mock_save_transaction,
        mock_get_customer,
        mock_get_stripe_info,
    ):
        with self.assertRaises(Exception):
            self.assertFalse(self.view.handle_transaction())
            mock_save_transaction.assert_not_called()
            mock_get_customer.assert_not_called()
            mock_get_stripe_info.assert_not_called()

    @patch("src.business.models.ProductComplementary.objects.get")
    @patch("src.business.views.CheckoutRedirectView.get_stripe_info")
    @patch("src.business.views.CheckoutRedirectView.get_customer")
    @patch("src.business.views.CheckoutRedirectView.save_transaction")
    def test_handle_transaction(
        self,
        mock_save_transaction,
        mock_get_customer,
        mock_get_stripe_info,
        mock_get_product,
    ):
        mock_get_product.return_value = "product_complementary"
        mock_get_stripe_info.return_value = "stripe_session", "stripe_customer"
        mock_get_customer.return_value = "customer"
        self.assertTrue(self.view.handle_transaction())
        mock_get_stripe_info.assert_called_once()
        mock_get_customer.assert_called_once_with(
            "stripe_session",
            "stripe_customer",
        )
        mock_save_transaction.assert_called_once_with(
            "stripe_session",
            "customer",
            "product_complementary",
        )

    def test_get_stripe_info(self):
        self.view.get_stripe_info()
        assert 1 == 2

    def test_get_customer(self):
        self.view.get_customer()
        assert 1 == 2

    def test_save_transaction(self):
        self.view.save_transaction()
        assert 1 == 2
