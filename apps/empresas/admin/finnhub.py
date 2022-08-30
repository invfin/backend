from django.contrib import admin
from django.db import models

from django_json_widget.widgets import JSONEditorWidget

from apps.empresas.models import (
    StatementsFinnhub,
    CompanyFinnhubProxy
)


class StatementsFinnhubInline(admin.StackedInline):
    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }
    model = StatementsFinnhub
    extra = 0
    jazzmin_tab_id = "statements"


@admin.register(CompanyFinnhubProxy)
class CompanyFinnhubProxyAdmin(admin.ModelAdmin):
    inlines = [StatementsFinnhubInline]

    fieldsets = (
        (
            "Company",
            {
                "classes": ("jazzmin-tab-general",),
                "fields": [
                    "ticker",
                    "name",
                ],
            },
        ),
    )

    list_display = [
        "id",
        "ticker",
        "name",
        "has_statements",
    ]

    search_fields = [
        "id",
        "ticker",
        "name",
    ]

    jazzmin_form_tabs = [
        ("general", "Company"),
        ("statements", "Statements")
        # ("income-statement", "Income Statement"),
        # ("balance-sheet", "Balance Sheet"),
        # ("cashflow-statement", "Cashflow Statement"),
    ]
