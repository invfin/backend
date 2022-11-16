from django.db.models import (
    SET_NULL,
    ForeignKey,
    IntegerField,
    DateField,
    DecimalField,
    Model,
    CharField,
    JSONField,
    ManyToManyField,
    PROTECT,
)


from apps.empresas.extensions.as_reported import IncomeStatementAsReportedExtended
from apps.empresas.managers import BaseStatementManager
from apps.general.mixins import BaseToAllMixin


class BaseStatement(Model, BaseToAllMixin):
    date = IntegerField(default=0)
    start_date = DateField(null=True, blank=True)
    end_date = DateField(null=True, blank=True)
    period = ForeignKey("periods.Period", on_delete=SET_NULL, null=True, blank=True)
    reported_currency = ForeignKey("currencies.Currency", on_delete=SET_NULL, null=True, blank=True)
    financial_data = JSONField()
    from_file = CharField(max_length=250, null=True, default="")
    from_folder = CharField(max_length=250, null=True, default="")
    objects = BaseStatementManager()

    class Meta:
        abstract = True
        get_latest_by = ["-date", "period"]
        ordering = ["-date", "period"]
        base_manager_name = "objects"

    def __str__(self) -> str:
        period = self.period if self.period else self.date
        return f"{self.company} - {period}"



class IncomeStatementAsReported(BaseStatement, IncomeStatementAsReportedExtended):
    company = ForeignKey(
        "empresas.Company",
        on_delete=SET_NULL,
        null=True,
        blank=True,
        related_name="inc_statements_as_reported",
    )
    fields = ManyToManyField(
        StatementField,
        blank=True,
        related_name="inc_statements_as_reported",
    )

    class Meta:
        db_table = "assets_income_statement_as_reported"


class BalanceSheetAsReported(BaseStatement):
    company = ForeignKey(
        "empresas.Company",
        on_delete=SET_NULL,
        null=True,
        blank=True,
        related_name="balance_sheets_as_reported",
    )

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

    class Meta:
        db_table = "assets_cashflow_statement_as_reported"
