from django.db.models import (
    SET_NULL,
    ForeignKey,
    IntegerField,
    DateField,
    Model,
    JSONField,
)


from apps.empresas.managers import BaseStatementManager
from apps.general.mixins import BaseToAllMixin


class BaseStatement(Model, BaseToAllMixin):
    date = IntegerField(default=0)
    start_date = DateField(null=True, blank=True)
    end_date = DateField(null=True, blank=True)
    period = ForeignKey("periods.Period", on_delete=SET_NULL, null=True, blank=True)
    reported_currency = ForeignKey("currencies.Currency", on_delete=SET_NULL, null=True, blank=True)
    objects = BaseStatementManager()

    class Meta:
        abstract = True
        get_latest_by = ["-date", "period"]
        ordering = ["-date", "period"]
        base_manager_name = "objects"

    def __str__(self) -> str:
        period = self.period if self.period else self.date
        return f"{self.company} - {period}"


class IncomeStatementAsReported(BaseStatement):
    company = ForeignKey(
        "empresas.Company",
        on_delete=SET_NULL,
        null=True,
        blank=True,
        related_name="inc_statements_as_reported",
    )
    financial_data = JSONField()

    class Meta:
        db_table = "assets_income_statement_as_reported"
        ordering = ["-date", "period"]


class BalanceSheetAsReported(BaseStatement):
    company = ForeignKey(
        "empresas.Company",
        on_delete=SET_NULL,
        null=True,
        blank=True,
        related_name="balance_sheets_as_reported",
    )
    financial_data = JSONField()

    class Meta:
        db_table = "assets_balance_sheet_as_reported"


class CashflowStatementAsReported(BaseStatement):
    company = ForeignKey(
        "empresas.Company",
        on_delete=SET_NULL,
        null=True,
        blank=True,
        related_name="cf_statements_as_reported",
    )
    financial_data = JSONField()

    class Meta:
        db_table = "assets_cashflow_statement_as_reported"
