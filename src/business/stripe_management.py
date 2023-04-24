from django.conf import settings

import stripe

from src.business.models import Customer, ProductComplementary, ProductComplementaryPaymentLink

STRIPE_PRIVATE = settings.STRIPE_PRIVATE
STRIPE_PUBLIC = settings.STRIPE_PUBLIC


class StripeManagement:
    stripe.api_key = STRIPE_PRIVATE
    stripe_product = stripe.Product
    stripe_price = stripe.Price
    stripe_customer = stripe.Customer

    def create_product(self, name: str, description: str, active: bool = False,) -> dict:
        return self.stripe_product.create(
            name=name,
            description=description,
            active=active,
        )

    def update_product(self, stripe_id: str, name: str, description: str, active: bool,) -> dict:
        return self.stripe_product.modify(
            sid=stripe_id,
            name=name,
            description=description,
            active=active,
        )

    def disable_product(self, stripe_id: str) -> dict:
        return self.stripe_product.modify(sid=stripe_id, active=False)

    def create_product_complementary(
        self,
        stripe_id: str,
        price: float,
        currency: str,
        is_recurring: bool = False,
        subscription_period: str = None,
        subscription_interval: int = None,
    ) -> dict:
        price_data = {
            "product": stripe_id,
            "unit_amount": int(price * 100),
            "currency": currency,
        }
        if is_recurring:
            price_data["recurring"] = {"interval": subscription_period, "interval_count": subscription_interval}

        price = self.stripe_price.create(**price_data)
        return price

    def update_product_complementary(
        self,
        stripe_id: str,
        active: bool = False,
    ) -> dict:
        price_data = {"sid": stripe_id, "active": active}

        price = self.stripe_price.modify(**price_data)
        return price

    def create_customer(self, currency: str, email: str, name: str) -> dict:
        return self.stripe_customer.create(currency=currency, email=email, name=name)

    def create_subscription(self, customer: Customer, stripe_price_obj: ProductComplementary) -> dict:
        subscription = stripe.Subscription.create(
            customer=customer.stripe_id,
            items=[
                {"price": stripe_price_obj.stripe_id},
            ],
        )
        return subscription

    def create_payment_link(self, stripe_price_obj: ProductComplementaryPaymentLink) -> dict:
        payment_link = stripe.PaymentLink.create(
            line_items=[
                {
                    "price": stripe_price_obj.product_complementary.stripe_id,
                    "quantity": 1,
                },
            ],
        )
        return payment_link
