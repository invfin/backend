from django.contrib import admin

from .models import FinancialObjectif, Income, Investment, Spend


@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "name",
        "amount",
        "description",
        "date",
        "currency",
        "is_recurrent",
    ]


@admin.register(Spend)
class SpendAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "name",
        "amount",
        "description",
        "date",
        "currency",
        "is_recurrent",
    ]


@admin.register(Investment)
class InvestmentAdmin(admin.ModelAdmin):
    list_display = ["user", "object"]


@admin.register(FinancialObjectif)
class FinancialObjectifAdmin(admin.ModelAdmin):
    list_display = [
        "user",
    ]
