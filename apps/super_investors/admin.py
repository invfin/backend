from django.contrib import admin

from .models import Superinvestor, SuperinvestorActivity, SuperinvestorHistory

class SuperinvestorHistoryInline(admin.StackedInline):
    model = SuperinvestorHistory
    extra = 0
    jazzmin_tab_id = "history"


class SuperinvestorActivityInline(admin.StackedInline):
    model = SuperinvestorActivity
    extra = 0
    jazzmin_tab_id = "activity"


@admin.register(Superinvestor)
class SuperinvestorAdmin(admin.ModelAdmin):
    inlines = [SuperinvestorHistoryInline, SuperinvestorActivityInline]
    list_display = [
        'id',
        'name',
        'fund_name',
        'slug',
        'image',
        'last_update',
        'has_error',
    ]
    list_editable = [
        'image'
    ]
    jazzmin_form_tabs = [
        ("general", "SuperInvestor"),
        ("activity", "Activity"),
        ("history", "History"),
    ]
