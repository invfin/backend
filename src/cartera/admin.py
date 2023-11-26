from django.contrib import admin

from .models import (
    FinancialObjectif,
    FirsttradeTransaction,
    Income,
    IngEsTransaction,
    Investment,
    Savings,
    Spendings,
    NetWorth,
)


@admin.register(NetWorth)
class NetWorthAdmin(admin.ModelAdmin):
    list_display = ["pk", "user", "period"]


@admin.register(IngEsTransaction)
class IngEsTransactionAdmin(admin.ModelAdmin):
    list_display = [
        "transaction_date",
        "category",
        "subcaterogy",
        "comment",
        "image",
        "amount",
        "file_path",
        "description",
        "balance",
    ]


@admin.register(FirsttradeTransaction)
class FirsttradeTransactionAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "symbol",
        "quantity",
        "price",
        "action",
        "description",
        "trade_date",
        "settled_date",
        "interest",
        "amount",
        "commission",
        "fee",
        "cusip",
        "record_type",
        "file_path",
    ]


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
        "net_worth",
    ]


@admin.register(Savings)
class SavingsAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "name",
        "amount",
        "description",
        "date",
        "currency",
        "is_recurrent",
        "net_worth",
    ]


@admin.register(Spendings)
class SpendingsAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "name",
        "amount",
        "description",
        "date",
        "currency",
        "is_recurrent",
        "net_worth",
    ]


@admin.register(Investment)
class InvestmentAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "object",
        "net_worth",
    ]


@admin.register(FinancialObjectif)
class FinancialObjectifAdmin(admin.ModelAdmin):
    list_display = [
        "user",
    ]
