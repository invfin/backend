from typing import Any, Dict
from src.empresas.models import Company
from src.empresas.querysets.statements import StatementQuerySet


class AveragesInterface:
    rentability_ratios: Dict[str, int | float]
    liquidity_ratios: Dict[str, int | float]
    margins: Dict[str, int | float]
    per_share_values: Dict[str, int | float]
    operation_risks_ratios: Dict[str, int | float]
    ev_ratios: Dict[str, int | float]
    growth_rates: Dict[str, int | float]
    price_to_ratios: Dict[str, int | float]
    efficiency_ratios: Dict[str, int | float]

    def __init__(self, statements: "StatementsInterface") -> None:
        for info in [
            "rentability_ratios",
            "liquidity_ratios",
            "margins",
            "per_share_values",
            "operation_risks_ratios",
            "ev_ratios",
            "growth_rates",
            "price_to_ratios",
            "efficiency_ratios",
        ]:
            setattr(self, info, getattr(statements, f"average_{info}")())
        return None


class StatementsInterface:
    inc_statements: StatementQuerySet
    balance_sheets: StatementQuerySet
    cf_statements: StatementQuerySet
    rentability_ratios: StatementQuerySet
    liquidity_ratios: StatementQuerySet
    margins: StatementQuerySet
    fcf_ratios: StatementQuerySet
    per_share_values: StatementQuerySet
    non_gaap_figures: StatementQuerySet
    operation_risks_ratios: StatementQuerySet
    ev_ratios: StatementQuerySet
    growth_rates: StatementQuerySet
    efficiency_ratios: StatementQuerySet
    price_to_ratios: StatementQuerySet

    def __init__(self, company: Company) -> None:
        for statement in [
            "inc_statements",
            "balance_sheets",
            "cf_statements",
            "rentability_ratios",
            "liquidity_ratios",
            "margins",
            "fcf_ratios",
            "per_share_values",
            "non_gaap_figures",
            "operation_risks_ratios",
            "ev_ratios",
            "growth_rates",
            "efficiency_ratios",
            "price_to_ratios",
        ]:
            setattr(self, statement, getattr(company, statement).yearly_exclude_ttm())
        return None


class CompanyInterface:
    company: Company
    statements: StatementsInterface
    averages: AveragesInterface

    def __init__(self, company: Company) -> None:
        self.company = company

    def __call__(self) -> "CompanyInterface":
        return self

    def load_statements(self) -> StatementsInterface:
        if not self.statements:
            self.statements = StatementsInterface(self.company)
        return self.statements

    def load_averages(self) -> AveragesInterface:
        if not self.averages:
            if not self.statements:
                self.load_statements()
            self.averages = AveragesInterface(self.statements)
        return self.averages
