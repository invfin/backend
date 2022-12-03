from django.apps import AppConfig
from django.core.checks import Tags, register


class AdminCustomConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "src.admin_custom"

    def ready(self):
        from .check import jazzmin_menu_check

        register(Tags.admin)(jazzmin_menu_check)
