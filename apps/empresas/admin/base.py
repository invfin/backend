from django.contrib import admin
from django.db import models

from django_json_widget.widgets import JSONEditorWidget

from apps.empresas.admin.filters.base import (
    NewCompanyToParseFilter,
    HasQuarterFilter,
)


class BaseJSONWidgetInline(admin.StackedInline):
    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }
    extra = 0


class BaseCompanyAdmin(admin.ModelAdmin):
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

    list_filter = [
        NewCompanyToParseFilter,
    ]

    list_display = [
        "id",
        "ticker",
        "name",
        "has_inc",
        "has_bs",
        "has_cf",
    ]

    search_fields = [
        "id",
        "ticker",
        "name",
    ]

    jazzmin_form_tabs = [
        ("general", "Company"),
        ("income-statement", "Income Statement"),
        ("balance-sheet", "Balance Sheet"),
        ("cashflow-statement", "Cashflow Statement"),
    ]

