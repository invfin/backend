from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from import_export.admin import ImportExportActionModelAdmin

from apps.users.forms import UserAdminChangeForm, UserAdminCreationForm

from .models import CreditUsageHistorial, MetaProfile, MetaProfileHistorial, Profile

User = get_user_model()


class CreditUsageHistorialInline(admin.StackedInline):
    model = CreditUsageHistorial
    verbose_name = "Credit Usage"
    verbose_name_plural = "Credit Usages"
    extra = 1
    fields = [
        'amount',
        'initial',
        'final',
        'movement',
        'move_source',
        'has_enought_credits',
    ]

    readonly_fields = [
        "date",
    ]

    jazzmin_tab_id = "credits"


@admin.register(User)
class UserAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    inlines = [CreditUsageHistorialInline]
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    fieldsets = (
        (
            "User information",
            {
                "classes": ("jazzmin-tab-general",),
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "username",
                    "password"
                )
            }
        ),
        (
            _("Type"), {"fields": ("is_writter", "just_newsletter")}
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

    list_display = [
        "username",
        "is_writter",
        "just_newsletter",
        "just_correction",
        "last_login",
        "date_joined"
    ]

    search_fields = [
        "first_name",
        "last_name",
        "username",
        "email"
    ]

    list_editable = [
        'is_writter',
        'just_newsletter',
        "just_correction"
    ]

    list_filter = [
        'is_writter',
        'just_newsletter',
        "just_correction"
    ]

    jazzmin_form_tabs = [
        ("general", "Personal Details"),
        ("meta", "Meta Details"),
        ("credits", "Credit Usage"),
    ]


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
        'reputation_score',
        'creditos',
        'ciudad',
        'recommended_by',
        'ref_code',
    ]

    search_fields = ['user__username']


@admin.register(MetaProfile)
class MetaProfileAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'ip',
        'country_code',
        'country_name',
        'dma_code',
        'is_in_european_union',
        'latitude',
        'longitude',
        'city',
        'region',
        'time_zone',
        'postal_code',
        'continent_code',
        'continent_name',
    ]


@admin.register(MetaProfileHistorial)
class MetaProfileHistorialAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
        'date',
        'meta_info'
    ]


# @admin.register(CreditUsageHistorial)
# class CreditUsageHistorialAdmin(admin.ModelAdmin):
#     list_display = [
#         'id',
#         'user',
#         'date',
#         'amount',
#         'initial',
#         'final',
#         'movement',
#         'move_source',
#         'has_enought_credits',
#     ]
