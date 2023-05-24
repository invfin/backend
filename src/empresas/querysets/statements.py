from typing import Dict, Union
from django.db.models import Avg

from src.general.managers import BaseQuerySet
from src.periods import constants


class BaseStatementQuerySet(BaseQuerySet):
    def quarterly(self) -> "BaseStatementQuerySet":
        return self.exclude(period__period=constants.PERIOD_FOR_YEAR)

    def yearly(self) -> "BaseStatementQuerySet":
        return self.filter(period__period=constants.PERIOD_FOR_YEAR)


class StatementQuerySet(BaseStatementQuerySet):
    def average_margins(self) -> Dict[str, Union[int, float]]:
        return self.aggregate(
            average_gross_margin=Avg("gross_margin"),
            average_ebitda_margin=Avg("ebitda_margin"),
            average_net_income_margin=Avg("net_income_margin"),
            average_fcf_margin=Avg("fcf_margin"),
            average_fcf_equity_to_net_income=Avg("fcf_equity_to_net_income"),
            average_unlevered_fcf_to_net_income=Avg("unlevered_fcf_to_net_income"),
            average_unlevered_fcf_ebit_to_net_income=Avg("unlevered_fcf_ebit_to_net_income"),
            average_owners_earnings_to_net_income=Avg("owners_earnings_to_net_income"),
        )

    def average_efficiency_ratios(self) -> Dict[str, Union[int, float]]:
        return self.aggregate(
            average_asset_turnover=Avg("asset_turnover"),
            average_inventory_turnover=Avg("inventory_turnover"),
            average_fixed_asset_turnover=Avg("fixed_asset_turnover"),
            average_accounts_payable_turnover=Avg("accounts_payable_turnover"),
            average_cash_conversion_cycle=Avg("cash_conversion_cycle"),
            average_days_inventory_outstanding=Avg("days_inventory_outstanding"),
            average_days_payables_outstanding=Avg("days_payables_outstanding"),
            average_days_sales_outstanding=Avg("days_sales_outstanding"),
            average_free_cashflow_to_operating_cashflow=Avg(
                "free_cashflow_to_operating_cashflow"
            ),
            average_operating_cycle=Avg("operating_cycle"),
        )

    def average_growth_rates(self) -> Dict[str, Union[int, float]]:
        return self.aggregate(
            average_revenue_growth=Avg("revenue_growth"),
            average_cost_revenue_growth=Avg("cost_revenue_growth"),
            average_operating_expenses_growth=Avg("operating_expenses_growth"),
            average_net_income_growth=Avg("net_income_growth"),
            average_shares_buyback=Avg("shares_buyback"),
            average_eps_growth=Avg("eps_growth"),
            average_fcf_growth=Avg("fcf_growth"),
            average_owners_earnings_growth=Avg("owners_earnings_growth"),
            average_capex_growth=Avg("capex_growth"),
            average_rd_expenses_growth=Avg("rd_expenses_growth"),
        )

    def average_per_share_values(self) -> Dict[str, Union[int, float]]:
        return self.aggregate(
            average_sales_ps=Avg("sales_ps"),
            average_book_ps=Avg("book_ps"),
            average_tangible_ps=Avg("tangible_ps"),
            average_fcf_ps=Avg("fcf_ps"),
            average_eps=Avg("eps"),
            average_cash_ps=Avg("cash_ps"),
            average_operating_cf_ps=Avg("operating_cf_ps"),
            average_capex_ps=Avg("capex_ps"),
            average_total_assets_ps=Avg("total_assets_ps"),
        )

    def average_price_to_ratios(self) -> Dict[str, Union[int, float]]:
        return self.aggregate(
            average_price_book=Avg("price_book"),
            average_price_cf=Avg("price_cf"),
            average_price_earnings=Avg("price_earnings"),
            average_price_earnings_growth=Avg("price_earnings_growth"),
            average_price_sales=Avg("price_sales"),
            average_price_total_assets=Avg("price_total_assets"),
            average_price_fcf=Avg("price_fcf"),
            average_price_operating_cf=Avg("price_operating_cf"),
            average_price_tangible_assets=Avg("price_tangible_assets"),
        )

    def average_liquidity_ratios(self) -> Dict[str, Union[int, float]]:
        return self.aggregate(
            average_cash_ratio=Avg("cash_ratio"),
            average_current_ratio=Avg("current_ratio"),
            average_quick_ratio=Avg("quick_ratio"),
            average_operating_cashflow_ratio=Avg("operating_cashflow_ratio"),
            average_debt_to_equity=Avg("debt_to_equity"),
        )

    def average_rentability_ratios(self) -> Dict[str, Union[int, float]]:
        return self.aggregate(
            average_roa=Avg("roa"),
            average_roe=Avg("roe"),
            average_roc=Avg("roc"),
            average_roce=Avg("roce"),
            average_rota=Avg("rota"),
            average_roic=Avg("roic"),
            average_nopat_roic=Avg("nopat_roic"),
            average_rogic=Avg("rogic"),
        )

    def average_operation_risks_ratios(self) -> Dict[str, Union[int, float]]:
        return self.aggregate(
            average_asset_coverage_ratio=Avg("asset_coverage_ratio"),
            average_cash_flow_coverage_ratios=Avg("cash_flow_coverage_ratios"),
            average_cash_coverage=Avg("cash_coverage"),
            average_debt_service_coverage=Avg("debt_service_coverage"),
            average_interest_coverage=Avg("interest_coverage"),
            average_operating_cashflow_ratio=Avg("operating_cashflow_ratio"),
            average_debt_ratio=Avg("debt_ratio"),
            average_long_term_debt_to_capitalization=Avg("long_term_debt_to_capitalization"),
            average_total_debt_to_capitalization=Avg("total_debt_to_capitalization"),
        )

    def average_ev_ratios(self) -> Dict[str, Union[int, float]]:
        return self.aggregate(
            average_ev_fcf=Avg("ev_fcf"),
            average_ev_operating_cf=Avg("ev_operating_cf"),
            average_ev_sales=Avg("ev_sales"),
            average_company_equity_multiplier=Avg("company_equity_multiplier"),
            average_ev_multiple=Avg("ev_multiple"),
        )
