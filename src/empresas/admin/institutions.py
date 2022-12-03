from django.contrib import admin
from django.db import models

from django_json_widget.widgets import JSONEditorWidget


from src.empresas.models import (
    InstitutionalOrganization,
    TopInstitutionalOwnership,
)


class TopInstitutionalOwnershipInline(admin.StackedInline):
    formfield_overrides = {
        models.JSONField: {"widget": JSONEditorWidget},
    }
    model = TopInstitutionalOwnership
    extra = 0
    jazzmin_tab_id = "top-institutionals"


@admin.register(InstitutionalOrganization)
class InstitutionalOrganizationInline(admin.ModelAdmin):
    inlines = [TopInstitutionalOwnershipInline]
    formfield_overrides = {
        models.JSONField: {"widget": JSONEditorWidget},
    }

    list_display = ["id", "name"]

    jazzmin_form_tabs = [
        ("general", "Institution"),
        ("top-institutionals", "Top Institutions"),
    ]
