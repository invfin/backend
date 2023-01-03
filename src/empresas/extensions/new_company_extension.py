import math
import operator

from typing import Dict

from django.db.models import QuerySet

import yahooquery as yq
import yfinance as yf

from src.empresas.outils.valuations import discounted_cashflow
from src.empresas.models import Company


class CompanyData:
    company: Company

    def __init__(self, company: Company):
        self.company = company

    def get_statements(self) -> Dict[str, QuerySet]:
        return{"inc_statements": self.company.inc_statements.yearly_exclude_ttm(),
         "balance_sheets": self.company.balance_sheets.yearly_exclude_ttm(),
         "cf_statements": self.company.cf_statements.yearly_exclude_ttm(),
         "rentability_ratios": self.company.rentability_ratios.yearly_exclude_ttm(),
         "liquidity_ratios": self.company.liquidity_ratios.yearly_exclude_ttm(),
         "margins": self.company.margins.yearly_exclude_ttm(),
         "fcf_ratios": self.company.fcf_ratios.yearly_exclude_ttm(),
         "per_share_values": self.company.per_share_values.yearly_exclude_ttm(),
         "non_gaap_figures": self.company.non_gaap_figures.yearly_exclude_ttm(),
         "operation_risks_ratios": self.company.operation_risks_ratios.yearly_exclude_ttm(),
         "ev_ratios": self.company.ev_ratios.yearly_exclude_ttm(),
         "growth_rates": self.company.growth_rates.yearly_exclude_ttm(),
         "efficiency_ratios": self.company.efficiency_ratios.yearly_exclude_ttm(),
         "price_to_ratios": self.company.price_to_ratios.yearly_exclude_ttm(), }
