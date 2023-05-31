from django.db.models import QuerySet

from src.empresas.models import Company


class CompanyInterface:
    company: Company
    inc_statements: QuerySet
    balance_sheets: QuerySet
    cf_statements: QuerySet
    rentability_ratios: QuerySet
    liquidity_ratios: QuerySet
    margins: QuerySet
    fcf_ratios: QuerySet
    per_share_values: QuerySet
    non_gaap_figures: QuerySet
    operation_risks_ratios: QuerySet
    ev_ratios: QuerySet
    growth_rates: QuerySet
    efficiency_ratios: QuerySet
    price_to_ratios: QuerySet

    def __init__(self, company: Company) -> None:
        self.company = company
        self.set_statements(company)

    def set_statements(self, company: Company) -> None:
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
