from django.conf import settings
from django.db.models import (
    PROTECT,
    SET_NULL,
    CharField,
    DateField,
    FloatField,
    ForeignKey,
    IntegerField,
    JSONField,
    ManyToManyField,
    SlugField,
    TextField,
)

from apps.empresas.extensions.as_reported import IncomeStatementAsReportedExtended
from apps.empresas.managers import BaseStatementManager
from apps.general.abstracts import AbstractTimeStampedModel


class StatementItemConcept(AbstractTimeStampedModel):
    concept = CharField(max_length=350)
    label = CharField(max_length=350)
    slug = SlugField(max_length=350)
    notes = TextField(null=True, default="")
    tooltip = TextField(null=True, default="")
    definition_path = SlugField(max_length=350)
    company = ForeignKey(
        "empresas.Company",
        on_delete=SET_NULL,
        null=True,
        related_name="unique_statements_items",
    )

    class Meta:
        db_table = "assets_as_repoted_statements_items_concepts"

    @property
    def is_unique_for_company(self) -> bool:
        return bool(self.company)

    @property
    def definition_link(self):
        return f"{settings.FULL_DOMAIN}{self.definition_path}"


class StatementItem(AbstractTimeStampedModel):
    concept = ForeignKey(StatementItemConcept, on_delete=PROTECT)
    value = FloatField()
    unit = CharField(max_length=50)
    currency = ForeignKey("currencies.Currency", on_delete=SET_NULL, null=True)

    class Meta:
        db_table = "assets_as_repoted_statements_items"


class BaseStatement(AbstractTimeStampedModel):
    date = IntegerField(default=0)
    start_date = DateField(null=True, blank=True)
    end_date = DateField(null=True, blank=True)
    period = ForeignKey("periods.Period", on_delete=SET_NULL, null=True, blank=True)
    reported_currency = ForeignKey("currencies.Currency", on_delete=SET_NULL, null=True, blank=True)
    financial_data = JSONField()
    fields = ManyToManyField(StatementItem, blank=True)
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
