from django.core.management import BaseCommand
from django.db.models import OuterRef, Subquery

from apps.empresas.models import (
    BalanceSheet,
    CashflowStatement,
    CompanyGrowth,
    EficiencyRatio,
    EnterpriseValueRatio,
    FreeCashFlowRatio,
    IncomeStatement,
    LiquidityRatio,
    MarginRatio,
    Company,
    NonGaap,
    OperationRiskRatio,
    PerShareValue,
    PriceToRatio,
    RentabilityRatio,
    BalanceSheetAsReported,
    IncomeStatementAsReported,
    CashflowStatementAsReported,
)
from apps.periods.models import Period


class Command(BaseCommand):
    def handle(self, *args, **options):
        base_statements = [IncomeStatement, BalanceSheet, CashflowStatement]
        for statement in [
            *base_statements,
            CompanyGrowth,
            EficiencyRatio,
            EnterpriseValueRatio,
            FreeCashFlowRatio,
            LiquidityRatio,
            MarginRatio,
            NonGaap,
            OperationRiskRatio,
            PerShareValue,
            PriceToRatio,
            RentabilityRatio,
        ]:
            statement.objects.filter(is_ttm=False, period__isnull=True).update(
                period=Subquery(
                    Period.objects.filter(
                        year=OuterRef("date"),
                        period=5,
                    ).values_list("id", flat=True)
                )
            )
        companies_as_rep = Company.objects.has_as_reported().exclude(name="From-as-reported")
        as_reported_statements = [
            (IncomeStatementAsReported, IncomeStatement),
            (BalanceSheetAsReported, BalanceSheet),
            (CashflowStatementAsReported, CashflowStatement),
        ]

        for as_reported, final in as_reported_statements:
            final.objects.yearly().filter(company__in=companies_as_rep).update(
                year=Subquery(
                    as_reported.objects.filter(company=OuterRef("company"), period=OuterRef("period"),).values_list(
                        "end_date",
                        flat=True,
                    )[:1]
                )
            )
