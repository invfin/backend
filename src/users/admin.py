from django.contrib import admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from import_export.admin import ImportExportActionModelAdmin
from allauth.account.models import EmailAddress

from src.business.admin import ProductCommentInline
from src.preguntas_respuestas.admin import AnswerInline, QuestionInline
from src.users.forms import UserAdminChangeForm, UserAdminCreationForm

from .models import CreditUsageHistorial, MetaProfileInfo, Profile, UsersCategory

User = get_user_model()


@admin.register(UsersCategory)
class UsersCategoryAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "slug",
    ]
    filter_horizontal = [
        "users",
    ]


class EmailAddressInline(admin.StackedInline):
    model = EmailAddress
    extra = 0
    jazzmin_tab_id = "emails"


class MetaProfileInfoInline(admin.StackedInline):
    model = MetaProfileInfo
    extra = 0
    fields = [
        "id",
        "ip",
        "country_code",
        "country_name",
        "dma_code",
        "is_in_european_union",
        "latitude",
        "longitude",
        "city",
        "region",
        "time_zone",
        "postal_code",
        "continent_code",
        "continent_name",
    ]
    readonly_fields = [
        "date",
    ]
    jazzmin_tab_id = "meta"


class CreditUsageHistorialInline(admin.StackedInline):
    model = CreditUsageHistorial
    verbose_name = "Credit Usage"
    verbose_name_plural = "Credit Usages"
    extra = 1
    fields = [
        "amount",
        "initial",
        "final",
        "movement",
        "move_source",
        "has_enought_credits",
    ]

    readonly_fields = [
        "date",
    ]

    jazzmin_tab_id = "credits"


class ProfileInline(admin.StackedInline):
    model = Profile
    verbose_name = "Profile"
    verbose_name_plural = "Profiles"
    fk_name = "user"
    fields = [
        "reputation_score",
        "creditos",
        "edad",
        "pais",
        "ciudad",
        "foto_perfil",
        "bio",
        "recommended_by",
        "ref_code",
    ]
    jazzmin_tab_id = "profile"


@admin.register(User)
class UserAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    inlines = [
        EmailAddressInline,
        CreditUsageHistorialInline,
        ProfileInline,
        MetaProfileInfoInline,
        ProductCommentInline,
        QuestionInline,
        AnswerInline,
    ]
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    fieldsets = (
        (
            "User information",
            {
                "classes": ("jazzmin-tab-general",),
                "fields": [
                    "first_name",
                    "last_name",
                    "email",
                    "username",
                    "is_writer",
                    "just_newsletter",
                ],
            },
        ),
        (
            "Login",
            {
                "classes": ("collapse", "jazzmin-tab-general"),
                "fields": (
                    "password",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "last_login",
                    "date_joined",
                ),
            },
        ),
        (
            "Permissions",
            {
                "classes": ("jazzmin-tab-permissions",),
                "fields": (
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )

    list_display = [
        "username",
        "is_writer",
        "just_newsletter",
        "just_correction",
        "for_testing",
        "is_bot",
        "last_login",
        "date_joined",
    ]

    search_fields = ["first_name", "last_name", "username", "email"]

    list_editable = [
        "is_writer",
        "just_newsletter",
        "just_correction",
        "for_testing",
        "is_bot",
    ]

    list_filter = [
        "is_writer",
        "just_newsletter",
        "just_correction",
        "for_testing",
        "is_bot",
        "is_active",
    ]

    jazzmin_form_tabs = [
        ("general", "User"),
        ("emails", "Emails"),
        ("profile", "Profile"),
        ("writer", "writer"),
        ("meta", "Meta"),
        ("credits", "Credits"),
        ("purchases", "Purchases"),
        ("product-complementary", "Complementary"),
        ("comments", "Reviews"),
        ("questions", "Questions"),
        ("answers", "Answers"),
        ("permissions", "Permissions"),
    ]
