from django.contrib import admin
from django.db import models

from import_export.admin import ImportExportActionModelAdmin
from django_json_widget.widgets import JSONEditorWidget

from .models import (
    Customer,
    Product,
    ProductComment,
    ProductComplementary,
    ProductComplementaryPaymentLink,
    ProductDiscount,
    StripeWebhookResponse,
    TransactionHistorial,
)


@admin.action(description='Save testing copy')
def create_copy_testing(modeladmin, request, queryset):
    historial = {
        'old_id': None,
        'new_id': None,
    }
    for query in queryset.values():
        query.pop('id')
        product_id = query.pop('product_id')
        query.pop('stripe_id')
        if product_id != historial['old_id']:
            historial['old_id'] = product_id
            product = Product.objects.filter(id=product_id).values()[0]
            product.pop('id')
            product.pop('stripe_id')
            product['for_testing'] = True
            new_product = Product.objects.create(**product)
            historial['new_id'] = new_product.id
        query['product_id'] = historial['new_id']
        query['for_testing'] = True
        queryset.model.objects.create(**query)


@admin.action(description='Create payment link')
def create_payment_link(modeladmin, request, queryset):
    for query in queryset:
        ProductComplementaryPaymentLink.objects.create(
            product_complementary=query
        )


class BaseStripeAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }
    list_display = [
        'id',
        'title',
        'stripe_id',
        'is_active',
        'for_testing',
        'created_at',
        'updated_at'
    ]
    list_editable = ['for_testing', 'is_active']
    list_filter = ['for_testing', 'is_active']
    search_fields= ['title']


class StripeWebhookResponseInline(admin.StackedInline):
    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }
    model = StripeWebhookResponse
    extra = 0
    jazzmin_tab_id = "webhook-response"


class ProductComplementaryInline(admin.StackedInline):
    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }
    model = ProductComplementary
    extra = 0
    jazzmin_tab_id = "product-complementary"


class ProductDiscountInline(admin.StackedInline):
    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }
    model = ProductDiscount
    extra = 0
    jazzmin_tab_id = "discounts"


class ProductCommentInline(admin.StackedInline):
    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }
    model = ProductComment
    extra = 0
    jazzmin_tab_id = "comments"


class TransactionHistorialInline(admin.StackedInline):
    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }
    model = TransactionHistorial
    extra = 0
    jazzmin_tab_id = "transactions-historial"


class ProductComplementaryPaymentLinkInline(admin.StackedInline):
    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }
    model = ProductComplementaryPaymentLink
    extra = 0
    jazzmin_tab_id = "payment-link"


@admin.register(ProductComplementary)
class ProductComplementaryAdmin(ImportExportActionModelAdmin, BaseStripeAdmin):
    actions =  [create_copy_testing, create_payment_link]
    inlines = [ProductComplementaryPaymentLinkInline]
    list_display = BaseStripeAdmin.list_display + [
        'product',
        'price',
        'payment_type',
        'currency',
    ]
    list_editable = []
    list_filter = []
    search_fields= []
    jazzmin_form_tabs = [
        ("general", "Customer"),
        ("payment-link", "Payment Link"),
    ]


@admin.register(Customer)
class CustomerAdmin(BaseStripeAdmin):
    inlines = [
        StripeWebhookResponseInline,
        TransactionHistorialInline,
    ]

    list_display = [
        'id',
        'user',
        'created_at',
        'stripe_id',
    ]

    list_editable = []

    list_filter = []

    search_fields = ['user__username']

    jazzmin_form_tabs = [
        ("general", "Customer"),
        ("transactions-historial", "Historial"),
        ("webhook-response", "Webhook Responses"),
    ]


@admin.register(Product)
class ProductAdmin(ImportExportActionModelAdmin, BaseStripeAdmin):
    inlines = [
        StripeWebhookResponseInline,
        ProductComplementaryInline,
        ProductDiscountInline,
        ProductCommentInline,
        TransactionHistorialInline,
    ]

    list_display = BaseStripeAdmin.list_display +[
        'slug',
        'visits',
    ]

    list_editable = [
        'for_testing',
        'is_active',
    ]

    list_filter = [
        'for_testing',
        'is_active',
    ]

    search_fields = [
        'title'
        ]

    jazzmin_form_tabs = [
        ("general", "Product"),
        ("product-complementary", "Complementary"),
        ("transactions-historial", "Historial"),
        ("comments", "Reviews"),
        ("discounts", "Discounts"),
        ("webhook-response", "Webhook Responses"),
    ]
