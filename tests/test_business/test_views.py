from unittest.mock import MagicMock, patch

from django.test import TestCase

import stripe

from src.business import constants
from src.business.models import Customer, Product, ProductComplementary
from src.business.views import CheckoutRedirectView
from src.currencies.models import Currency
from src.users.models import User
from tests.data.business import checkout_session


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
        cls.request = MagicMock(
            GET={"prod": cls.base_prod_comp.id, "session_id": "cs_test_a1efUTq7VYePHRp07jtfRK5UmIOepUGV1HMgpA"}
        )
        cls.stripe_session = stripe.checkout.Session()
        cls.stripe_session.update(checkout_session.checkout_session)
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

    @patch("stripe.Customer.retrieve")
    @patch("stripe.checkout.Session.retrieve")
    def test_get_stripe_info(
        self,
        mock_session_retrieve,
        mock_customer_retrieve,
    ):
        session = MagicMock(customer="customer")
        stripe_customer = MagicMock()
        mock_session_retrieve.return_value = session
        mock_customer_retrieve.return_value = stripe_customer
        result_session, result_stripe_customer = self.view.get_stripe_info()
        mock_session_retrieve.assert_called_once_with("cs_test_a1efUTq7VYePHRp07jtfRK5UmIOepUGV1HMgpA")
        mock_customer_retrieve.assert_called_once_with("customer")
        self.assertEqual(result_session, session)
        self.assertEqual(result_stripe_customer, stripe_customer)

    @patch("src.users.models.User.objects.get_or_create_quick_user")
    @patch("src.business.models.Customer.objects.get_or_create")
    def test_get_customer(
        self,
        mock_get_or_create,
        mock_get_or_create_quick_user,
    ):
        user = User()
        customer = Customer()
        stripe_session = MagicMock(customer="customer")
        stripe.Customer()
        mock_get_or_create_quick_user.return_value = user
        mock_get_or_create.return_value = customer, True
        result = self.view.get_customer(
            stripe_session,
            dict(email="customer@gmail.com"),
        )
        mock_get_or_create_quick_user.assert_called_once_with(
            self.request,
            "customer@gmail.com",
        )
        mock_get_or_create.assert_called_once_with(
            user=user,
            defaults={"stripe_id": stripe_session.customer},
        )
        self.assertEqual(result, customer)

    @patch("src.currencies.models.Currency.objects.get_or_create")
    @patch("src.business.models.TransactionHistorial.objects.create")
    def test_save_transaction(
        self,
        mock_create,
        mock_get_or_create,
    ):
        currency = Currency()
        customer = Customer(user=User(username="hey"))
        mock_get_or_create.return_value = currency, True
        self.view.save_transaction(
            self.stripe_session,
            customer,
            self.base_prod_comp,
        )
        mock_get_or_create.assert_called_once_with(currency="USD")
        mock_create.assert_called_once_with(
            product=self.base_prod_comp.product,
            product_complementary=self.base_prod_comp,
            customer=customer,
            payment_method="card",
            currency=currency,
            final_amount=50.0,
            stripe_response=self.stripe_session,
        )
