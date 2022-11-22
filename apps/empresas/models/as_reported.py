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

from apps.empresas.extensions.as_reported import (
    IncomeStatementAsReportedExtended,
    BalanceSheetAsReportedExtended,
    CashflowStatementAsReportedExtended
)
from apps.empresas.managers import AsReportedStatementManager
from apps.general.abstracts import AbstractTimeStampedModel


class StatementItemConcept(AbstractTimeStampedModel):
    concept = CharField(max_length=2000)
    label = CharField(max_length=2000)
    concept_slug = CharField(max_length=2000)
    label_slug = CharField(max_length=2000)
    notes = TextField(null=True, default="")
    tooltip = TextField(null=True, default="")
    definition_path = SlugField(max_length=350)
    company = ForeignKey(
        "empresas.Company",
        on_delete=SET_NULL,
        null=True,
        related_name="unique_statements_items",
    )
    corresponding_final_item = CharField(max_length=350, null=True, default="")

    class Meta:
        db_table = "assets_as_repoted_statements_items_concepts"

    def __str__(self) -> str:
        return self.label

    @property
    def has_final_item_mapped(self) -> bool:
        return bool(self.corresponding_final_item)

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

    def __str__(self) -> str:
        return self.concept.label


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
    objects = AsReportedStatementManager()

    class Meta:
        abstract = True
        get_latest_by = ["-date", "period"]
        ordering = ["-date", "period"]
        base_manager_name = "objects"

    def __str__(self) -> str:
        period = self.period if self.period else self.date
        return f"{self.company} - {period}"

    @property
    def number_final_items_mapped(self) -> int:
        return self.fields.filter(corresponding_final_item__isnull=False).count()


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


class BalanceSheetAsReported(BaseStatement, BalanceSheetAsReportedExtended):
    company = ForeignKey(
        "empresas.Company",
        on_delete=SET_NULL,
        null=True,
        blank=True,
        related_name="balance_sheets_as_reported",
    )

    class Meta:
        db_table = "assets_balance_sheet_as_reported"


class CashflowStatementAsReported(BaseStatement, CashflowStatementAsReportedExtended):
    company = ForeignKey(
        "empresas.Company",
        on_delete=SET_NULL,
        null=True,
        blank=True,
        related_name="cf_statements_as_reported",
    )

    class Meta:
        db_table = "assets_cashflow_statement_as_reported"
