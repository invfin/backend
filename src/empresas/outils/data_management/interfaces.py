from typing import Optional, Union, Dict
from src.empresas.models import Company
from src.empresas.querysets.statements import StatementQuerySet


RATIOS_VALUES = [
            "rentability_ratios",
            "liquidity_ratios",
            "margins",
            "per_share_values",
            "operation_risks_ratios",
            "ev_ratios",
            "growth_rates",
            "price_to_ratios",
            "efficiency_ratios",
        ]

STATEMENTS = [
            "inc_statements",
            "balance_sheets",
            "cf_statements",
            "non_gaap_figures",
            "fcf_ratios",
        ] + RATIOS_VALUES


class AveragesInterface:
    rentability_ratios: Dict[str, Union[int, float]]
    liquidity_ratios: Dict[str, Union[int, float]]
    margins: Dict[str, Union[int, float]]
    per_share_values: Dict[str, Union[int, float]]
    operation_risks_ratios: Dict[str, Union[int, float]]
    ev_ratios: Dict[str, Union[int, float]]
    growth_rates: Dict[str, Union[int, float]]
    price_to_ratios: Dict[str, Union[int, float]]
    efficiency_ratios: Dict[str, Union[int, float]]

    def __init__(self, statements: "StatementsInterface") -> None:
        for info in RATIOS_VALUES:
            statement = getattr(statements, info)
            setattr(self, info, getattr(statement, f"average_{info}")())
        return None

    def join_averages(self) -> Dict[str, Union[int, float]]:
        final: Dict[str, Union[int, float]] = {}
        for info in RATIOS_VALUES:
            final |= getattr(self, info)
        return final


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
        for statement in STATEMENTS:
            setattr(self, statement, getattr(company, statement).yearly_exclude_ttm())
        return None


class CompanyInterface:
    company: Company
    statements: Optional[StatementsInterface] = None
    averages: Optional[AveragesInterface] = None

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
            self.averages = AveragesInterface(self.load_statements())
        return self.averages
