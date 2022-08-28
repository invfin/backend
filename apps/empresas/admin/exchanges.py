from django.contrib import admin

from apps.empresas.models import (
    Exchange,
    ExchangeOrganisation,
)


@admin.register(Exchange)
class ExchangeAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'exchange_ticker',
        'exchange',
        'country',
        'main_org'
    ]
    search_fields = ['main_org_name']


@admin.register(ExchangeOrganisation)
class ExchangeOrganisationAdmin(admin.ModelAdmin):
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
