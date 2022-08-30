from django.contrib import admin

from apps.empresas.models import (
    Exchange,
    ExchangeOrganisation,
)


class ExchangeInline(admin.StackedInline):
    model = Exchange
    fields = [
        "exchange_ticker",
        "exchange",
        "country",
        "data_source",
    ]


@admin.register(ExchangeOrganisation)
class ExchangeOrganisationAdmin(admin.ModelAdmin):
    inlines = [ExchangeInline]
    list_display = [
        'id',
        'name',
        'image',
        'sub_exchange1',
        'sub_exchange2',
        'order',
    ]
    list_editable = ['order']
    search_fields = ['name']
