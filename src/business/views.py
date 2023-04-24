from typing import Tuple

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import RedirectView

import stripe

from src.business.models import Customer, Product, ProductComplementary, TransactionHistorial
from src.currencies.models import Currency
from src.seo.views import SEODetailView, SEOListView, SEOTemplateView

User = get_user_model()
stripe.api_key = settings.STRIPE_PRIVATE
STRIPE_PUBLIC_KEY = settings.STRIPE_PUBLIC
IS_TESTING = settings.DEBUG and settings.CURRENT_DOMAIN != settings.MAIN_DOMAIN


class ProductsListView(SEOListView):
    model = Product
    template_name = "product_list.html"
    meta_description = "Las mejores herramientas para ser un mejor inversor, todo, al mejor precio, gratis."
    meta_title = "Las herramientas inteligentes para invertir como un experto"
    context_object_name = "products"
    ordering = ["-visits"]

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True, for_testing=IS_TESTING)


class ProductDetailView(SEODetailView):
    model = Product
    update_visits = True
    template_name = "product_detail.html"

    def get_object(self, *args):
        return self.model._default_manager.get(
            slug=self.kwargs["slug"],
            is_active=True,
            for_testing=IS_TESTING,
        )

    def update_views(self, instance):
        instance.visits += 1
        instance.save(update_fields=["visits"])


class CreateCheckoutView(SEODetailView):
    """
    This view is never actually rendered.
    It just gets the model asked and the redirects to the stripe checkout page.
    """

    model = ProductComplementary
    meta_description = "Las mejores herramientas para ser un mejor inversor, todo, al mejor precio, gratis."
    meta_title = "Caja"

    def get(self, request, *args, **kwargs) -> HttpResponse:
        product = self.get_object()
        success_path = reverse("business:order_success")
        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        "price": product.stripe_id,
                        "quantity": 1,
                    }
                ],
                payment_method_types=["card"],
                mode=product.payment_type,
                success_url=f"{settings.FULL_DOMAIN}{success_path}?prod={product.id}"
                + "&session_id={CHECKOUT_SESSION_ID}",
                cancel_url=f"{settings.FULL_DOMAIN}/la-mejor-herramienta-para-invertir-es/{product.product.slug}",
            )

        except Exception as e:
            return str(e)
        return redirect(checkout_session.url, code=303)


class CheckoutRedirectView(RedirectView):
    """
    This one redirects once the purchase has been done.
    """

    def get(self, request, *args, **kwargs):
        self.handle_messages()
        return HttpResponseRedirect(reverse("business:all_products"))

    def handle_messages(self):
        if self.handle_transaction():
            messages.success(
                self.request,
                "Gracias por tu confianza.",
            )
        else:
            messages.error(
                self.request,
                "Lo lamentamos ha sucedido un error. Lo estamos resolviendo",
            )

    def handle_transaction(self) -> bool:
        try:
            product_complementary = ProductComplementary.objects.get(
                pk=self.request.GET.get("prod"),
            )
            stripe_session, stripe_customer = self.get_stripe_info()
            customer = self.get_customer(stripe_session, stripe_customer)
            self.save_transaction(stripe_session, customer, product_complementary)
            return True
        except Exception:
            return False

    def get_stripe_info(self) -> Tuple[stripe.checkout.Session, stripe.Customer]:
        session = stripe.checkout.Session.retrieve(self.request.GET.get("session_id"))
        stripe_customer = stripe.Customer.retrieve(session.customer)
        return session, stripe_customer

    def get_customer(
        self,
        stripe_session: stripe.checkout.Session,
        stripe_customer: stripe.Customer,
    ) -> Customer:
        user = User.objects.get_or_create_quick_user(
            self.request,
            stripe_customer["email"],
        )
        customer, created = Customer.objects.get_or_create(
            user=user,
            defaults={
                "stripe_id": stripe_session.customer,
            },
        )
        return customer

    def save_transaction(
        self,
        stripe_response: stripe.checkout.Session,
        customer: Customer,
        product_complementary: ProductComplementary,
    ) -> None:
        currency, created = Currency.objects.get_or_create(currency=stripe_response["currency"].upper())
        TransactionHistorial.objects.create(
            product=product_complementary.product,
            product_complementary=product_complementary,
            customer=customer,
            payment_method=stripe_response["payment_method_types"][0],
            currency=currency,
            final_amount=(stripe_response["amount_total"] / 100),
            stripe_response=stripe_response,
        )


class CreateUserFromCustomerRecentPurchase(SEOTemplateView):
    template_name = "post_purchase_waiting.html"

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
