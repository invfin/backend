from typing import Dict, List, Tuple, Union

from django.db.models import QuerySet
from django.utils import timezone

from src.periods.constants import PERIOD_FOR_YEAR

from .efficiency_ratios import EfficiencyRatios
from .enterprise_value_ratios import EnterpriseValueRatios
from .free_cashflow_ratios import FreeCashFlowRatios
from .growth_rates import GrowthRates
from .liquidity_ratios import LiquidityRatios
from .margins import Margins
from .non_gaap import NonGaap
from .operation_risk_ratios import OperationRiskRatios
from .other_ratios import OtherRatios
from .per_share_values import PerShareValues
from .rentability_ratios import RentabilityRatios
from .valuation_ratios import ValuationRatios


class CalculateFinancialRatios(
    ValuationRatios,
    EfficiencyRatios,
    LiquidityRatios,
    OperationRiskRatios,
    PerShareValues,
    RentabilityRatios,
    Margins,
    FreeCashFlowRatios,
    NonGaap,
    OtherRatios,
    GrowthRates,
    EnterpriseValueRatios,
):
    def __init__(self, company):
        self.company = company

    @classmethod
    def filter_previous_year_data(
        cls, data: Dict[str, Union[int, float]]
    ) -> Dict[str, Union[int, float]]:
        last_year_inventory = data.get("inventory", 0)
        last_year_accounts_payable = data.get("accounts_payable", 0)
        last_year_revenue = data.get("revenue", 0)
        last_year_net_income = data.get("net_income", 0)
        last_year_fcf = data.get("free_cash_flow", 0)
        last_year_capex = data.get("capital_expenditure", 0)
        last_year_shares_outstanding = data.get("weighted_average_shares_outstanding", 0)
        last_year_cost_expense = data.get("cost_and_expenses", 0)
        last_year_cost_revenue = data.get("cost_of_revenue", 0)
        last_year_eps = cls.calculate_eps(
            data.get("net_income", 0),
            data.get("weighted_average_shares_outstanding", 0),
        )
        last_year_research_dev = data.get("rd_expenses", 0)
        last_year_fixed_assets = data.get("property_plant_equipment_net", 0)
        last_year_assets = data.get("total_assets", 0)
        last_year_owner_earnings = cls.calculate_owners_earnings(
            data.get("net_income", 0),
            data.get("depreciation_and_amortization", 0),
            data.get("change_in_working_capital", 0),
            data.get("capital_expenditure", 0),
        )
        last_year_current_assets = data.get("total_current_assets", 0)
        last_year_current_liabilities = data.get("total_current_liabilities", 0)

        return {
            "last_year_inventory": last_year_inventory,
            "last_year_accounts_payable": last_year_accounts_payable,
            "last_year_revenue": last_year_revenue,
            "last_year_net_income": last_year_net_income,
            "last_year_fcf": last_year_fcf,
            "last_year_capex": last_year_capex,
            "last_year_shares_outstanding": last_year_shares_outstanding,
            "last_year_cost_expense": last_year_cost_expense,
            "last_year_cost_revenue": last_year_cost_revenue,
            "last_year_eps": last_year_eps,
            "last_year_research_dev": last_year_research_dev,
            "last_year_fixed_assets": last_year_fixed_assets,
            "last_year_assets": last_year_assets,
            "last_year_owner_earnings": last_year_owner_earnings,
            "last_year_current_assets": last_year_current_assets,
            "last_year_current_liabilities": last_year_current_liabilities,
        }

    def split_statements_by_year(
        self,
        year: int = timezone.now().year,
        period: int = PERIOD_FOR_YEAR,
    ) -> Tuple[List, List]:
        current_year = year
        previous_year = current_year - 1
        inc_statements = self.company.inc_statements.filter(period__period=period)
        balance_sheets = self.company.balance_sheets.filter(period__period=period)
        cf_statements = self.company.cf_statements.filter(period__period=period)
        return (
            [
                inc_statements.filter(period__year=current_year).first(),
                balance_sheets.filter(period__year=current_year).first(),
                cf_statements.filter(period__year=current_year).first(),
            ],
            [
                inc_statements.filter(period__year=previous_year).first(),
                balance_sheets.filter(period__year=previous_year).first(),
                cf_statements.filter(period__year=previous_year).first(),
            ],
        )

    @classmethod
    def prepare_base_data(
        cls,
        current_income_statements: Union[List, QuerySet],
        current_balance_sheets: Union[List, QuerySet],
        current_cashflow_statements: Union[List, QuerySet],
        previous_income_statements: Union[List, QuerySet],
        previous_balance_sheets: Union[List, QuerySet],
        previous_cashflow_statements: Union[List, QuerySet],
        current_price: Dict[str, Union[int, float]],
    ) -> Dict[str, Union[int, float]]:
        to_clean_previous_data = {
            **previous_income_statements[0],
            **previous_balance_sheets[0],
            **previous_cashflow_statements[0],
        }
        previous_year_data = cls.filter_previous_year_data(to_clean_previous_data)
        current_year_data = {
            **current_income_statements[0],
            **current_balance_sheets[0],
            **current_cashflow_statements[0],
        }
        return {
            **previous_year_data,
            **current_year_data,
            **current_price,
        }

    @classmethod
    def calculate_other_ratios(
        cls, data: Dict[str, Union[int, float]]
    ) -> Dict[str, Union[int, float]]:
        average_fixed_assets = cls.calculate_average_fixed_assets(
            data.get("last_year_fixed_assets", 0),
            data.get("property_plant_equipment_net", 0),
        )
        average_assets = cls.calculate_average_assets(
            data.get("last_year_assets", 0),
            data.get("total_assets", 0),
        )
        net_working_capital = cls.calculate_net_working_capital(
            data.get("total_current_assets", 0),
            data.get("total_current_liabilities", 0),
        )
        change_in_working_capital = cls.calculate_change_in_working_capital(
            net_working_capital,
            data.get("last_year_current_assets", 0),
            data.get("last_year_current_liabilities", 0),
        )
        gross_invested_capital = cls.calculate_gross_invested_capital(
            net_working_capital,
            data.get("property_plant_equipment_net", 0),
            data.get("depreciation_and_amortization", 0),
        )
        effective_tax_rate = cls.calculate_effective_tax_rate(
            data.get("income_tax_expense", 0),
            data.get("operating_income", 0),
        )
        net_tangible_equity = cls.calculate_net_tangible_equity(
            data.get("total_current_assets", 0),
            data.get("property_plant_equipment_net", 0),
            data.get("total_liabilities", 0),
        )
        nopat = cls.calculate_nopat(
            data.get("operating_income", 0),
            data.get("income_tax_expense", 0),
        )
        debt_and_equity = cls.calculate_debt_and_equity(
            data.get("total_debt", 0),
            data.get("total_stockholders_equity", 0),
        )
        non_cash_working_capital = cls.calculate_non_cash_working_capital(
            net_working_capital,
            data.get("cash_and_cash_equivalents", 0),
        )
        common_equity = cls.calculate_common_equity(
            data.get("common_stocks", 0),
            data.get("current_price", 0),
            data.get("retained_earnings", 0),
        )
        preferred_equity = cls.calculate_preferred_equity(
            # let's use common_stocks if we don't have preferred stocks
            data.get("preferred_stocks", data.get("common_stocks", 0)),
            data.get("preferred_share_price", data.get("current_price", 0)),
        )
        invested_capital = cls.calculate_invested_capital(
            data.get("long_term_debt", 0),
            common_equity,
            preferred_equity,
        )

        return {
            "average_fixed_assets": average_fixed_assets,
            "average_assets": average_assets,
            "net_working_capital": net_working_capital,
            "change_in_working_capital": change_in_working_capital,
            "gross_invested_capital": gross_invested_capital,
            "effective_tax_rate": effective_tax_rate,
            "net_tangible_equity": net_tangible_equity,
            "nopat": nopat,
            "debt_and_equity": debt_and_equity,
            "non_cash_working_capital": non_cash_working_capital,
            "invested_capital": invested_capital,
            "common_equity": common_equity,
            "preferred_equity": preferred_equity,
        }

    @classmethod
    def calculate_rentability_ratios(
        cls, data: Dict[str, Union[int, float]]
    ) -> Dict[str, Union[int, float]]:
        roa = cls.calculate_roa(data.get("net_income", 0), data.get("total_assets", 0))
        roe = cls.calculate_roe(
            data.get("net_income", 0),
            data.get("total_stockholders_equity", 0),
        )
        roc = cls.calculate_roc(data.get("operating_income", 0), data.get("total_assets", 0))
        rota = cls.calculate_rota(data.get("net_income", 0), data.get("tangible_assets", 0))
        roic = cls.calculate_roic(
            data.get("net_income", 0),
            data.get("dividends_paid", 0),
            data.get("invested_capital", 0),
        )
        nopat_roic = cls.calculate_nopat_roic(
            data.get("nopat", 0), data.get("invested_capital", 0)
        )
        rogic = cls.calculate_rogic(
            data.get("nopat", 0), data.get("gross_invested_capital", 0)
        )
        return {
            "roa": roa,
            "roe": roe,
            "roc": roc,
            "roce": cls.calculate_roce(
                data.get("operating_income", 0),
                data.get("capital_employed", 0),
            ),
            "rota": rota,
            "roic": roic,
            "nopat_roic": nopat_roic,
            "rogic": rogic,
        }

    @classmethod
    def calculate_liquidity_ratios(
        cls, data: Dict[str, Union[int, float]]
    ) -> Dict[str, Union[int, float]]:
        cash_ratio = cls.calculate_cash_ratio(
            data.get("cash_and_cash_equivalents", 0),
            data.get("total_current_liabilities", 0),
        )
        current_ratio = cls.calculate_current_ratio(
            data.get("total_current_assets", 0),
            data.get("total_current_liabilities", 0),
        )
        quick_ratio = cls.calculate_quick_ratio(
            data.get("net_receivables", 0),
            data.get("cash_and_short_term_investments", 0),
            data.get("total_current_liabilities", 0),
        )
        operating_cashflow_ratio = cls.calculate_operating_cashflow_ratio(
            data.get("net_cash_provided_by_operating_activities", 0),
            data.get("total_current_liabilities", 0),
        )
        debt_to_equity = cls.calculate_debt_to_equity(
            data.get("total_liabilities", 0),
            data.get("total_stockholders_equity", 0),
        )

        return {
            "cash_ratio": cash_ratio,
            "current_ratio": current_ratio,
            "quick_ratio": quick_ratio,
            "operating_cashflow_ratio": operating_cashflow_ratio,
            "debt_to_equity": debt_to_equity,
        }

    @classmethod
    def calculate_margin_ratios(
        cls, data: Dict[str, Union[int, float]]
    ) -> Dict[str, Union[int, float]]:
        gross_margin = cls.calculate_gross_margin(
            data.get("gross_profit", 0),
            data.get("revenue", 0),
        )
        ebitda_margin = cls.calculate_ebitda_margin(
            data.get("ebitda", 0),
            data.get("revenue", 0),
        )
        net_income_margin = cls.calculate_net_income_margin(
            data.get("net_income", 0),
            data.get("revenue", 0),
        )
        fcf_margin = cls.calculate_fcf_margin(
            data.get("free_cash_flow", 0),
            data.get("revenue", 0),
        )
        fcf_equity_to_net_income = cls.calculate_fcf_equity_to_net_income(
            data.get("fcf_equity", 0),
            data.get("net_income", 0),
        )
        unlevered_fcf_to_net_income = cls.calculate_unlevered_fcf_to_net_income(
            data.get("unlevered_fcf", 0),
            data.get("net_income", 0),
        )
        unlevered_fcf_ebit_to_net_income = cls.calculate_unlevered_fcf_ebit_to_net_income(
            data.get("unlevered_fcf_ebit", 0),
            data.get("net_income", 0),
        )
        owners_earnings_to_net_income = cls.calculate_owners_earnings_to_net_income(
            data.get("owners_earnings", 0),
            data.get("net_income", 0),
        )

        return {
            "gross_margin": gross_margin,
            "ebitda_margin": ebitda_margin,
            "net_income_margin": net_income_margin,
            "fcf_margin": fcf_margin,
            "fcf_equity_to_net_income": fcf_equity_to_net_income,
            "unlevered_fcf_to_net_income": unlevered_fcf_to_net_income,
            "unlevered_fcf_ebit_to_net_income": unlevered_fcf_ebit_to_net_income,
            "owners_earnings_to_net_income": owners_earnings_to_net_income,
        }

    @classmethod
    def calculate_free_cashflow_ratios(
        cls, data: Dict[str, Union[int, float]]
    ) -> Dict[str, Union[int, float]]:
        fcf_equity = cls.calculate_fcf_equity(
            data.get("net_cash_provided_by_operating_activities", 0),
            data.get("capital_expenditure", 0),
            data.get("debt_repayment", 0),
        )
        unlevered_fcf = cls.calculate_unlevered_fcf(
            data.get("nopat", 0),
            data.get("depreciation_and_amortization", 0),
            data.get("change_in_working_capital", 0),
            data.get("capital_expenditure", 0),
        )
        unlevered_fcf_ebit = cls.calculate_unlevered_fcf_ebit(
            data.get("operating_income", 0),
            data.get("depreciation_and_amortization", 0),
            data.get("deferred_income_tax", 0),
            data.get("change_in_working_capital", 0),
            data.get("capital_expenditure", 0),
        )
        owners_earnings = cls.calculate_owners_earnings(
            data.get("net_income", 0),
            data.get("depreciation_and_amortization", 0),
            data.get("change_in_working_capital", 0),
            data.get("capital_expenditure", 0),
        )
        return {
            "fcf_equity": fcf_equity,
            "unlevered_fcf": unlevered_fcf,
            "unlevered_fcf_ebit": unlevered_fcf_ebit,
            "owners_earnings": owners_earnings,
        }

    @classmethod
    def calculate_per_share_value(
        cls, data: Dict[str, Union[int, float]]
    ) -> Dict[str, Union[int, float]]:
        sales_ps = cls.calculate_sales_ps(
            data.get("revenue", 0),
            data.get("weighted_average_shares_outstanding", 0),
        )
        book_ps = cls.calculate_book_ps(
            data.get("total_stockholders_equity", 0),
            data.get("weighted_average_shares_outstanding", 0),
        )
        tangible_ps = cls.calculate_tangible_ps(
            data.get("net_tangible_equity", 0),
            data.get("weighted_average_shares_outstanding", 0),
        )
        fcf_ps = cls.calculate_fcf_ps(
            data.get("free_cash_flow", 0),
            data.get("weighted_average_shares_outstanding", 0),
        )
        eps = cls.calculate_eps(
            data.get("net_income", 0),
            data.get("weighted_average_shares_outstanding", 0),
        )
        cash_ps = cls.calculate_cash_ps(
            data.get("cash_and_short_term_investments", 0),
            data.get("weighted_average_shares_outstanding", 0),
        )
        operating_cf_ps = cls.calculate_operating_cf_ps(
            data.get("net_cash_provided_by_operating_activities", 0),
            data.get("weighted_average_shares_outstanding", 0),
        )
        capex_ps = cls.calculate_capex_ps(
            data.get("capital_expenditure", 0),
            data.get("weighted_average_shares_outstanding", 0),
        )
        total_assets_ps = cls.calculate_total_assets_ps(
            data.get("total_assets", 0),
            data.get("weighted_average_shares_outstanding", 0),
        )

        return {
            "sales_ps": sales_ps,
            "book_ps": book_ps,
            "tangible_ps": tangible_ps,
            "fcf_ps": fcf_ps,
            "eps": eps,
            "cash_ps": cash_ps,
            "operating_cf_ps": operating_cf_ps,
            "capex_ps": capex_ps,
            "total_assets_ps": total_assets_ps,
        }

    @classmethod
    def calculate_non_gaap(
        cls, data: Dict[str, Union[int, float]]
    ) -> Dict[str, Union[int, float]]:
        normalized_income = cls.calculate_normalized_income(
            data.get("net_income", 0),
            data.get("total_other_income_expenses_net", 0),
        )
        effective_tax_rate = cls.calculate_effective_tax_rate(
            data.get("income_tax_expense", 0),
            data.get("operating_income", 0),
        )

        net_working_capital = cls.calculate_net_working_capital(
            data.get("total_current_assets", 0),
            data.get("total_current_liabilities", 0),
        )
        average_inventory = cls.calculate_average_inventory(
            data.get("last_year_inventory", 0),
            data.get("inventory", 0),
        )
        average_accounts_payable = cls.calculate_average_accounts_payable(
            data.get("last_year_accounts_payable", 0),
            data.get("accounts_payable", 0),
        )
        divs_per_share = cls.calculate_divs_per_share(
            data.get("dividends_paid", 0),
            data.get("common_stock", 0),
        )
        dividend_yield = cls.calculate_dividend_yield(
            divs_per_share,
            data.get("current_price", 0),
        )
        earnings_yield = cls.calculate_earnings_yield(
            data.get("eps", 0),
            data.get("current_price", 0),
        )
        fcf_yield = cls.calculate_fcf_yield(
            data.get("fcf_ps", 0),
            data.get("current_price", 0),
        )
        income_quality = cls.calculate_income_quality(
            data.get("net_cash_provided_by_operating_activities", 0),
            data.get("net_income", 0),
        )

        invested_capital = cls.calculate_invested_capital(
            data.get("property_plant_equipment_net", 0),
            data.get("net_working_capital", 0),
            data.get("cash_and_cash_equivalents", 0),
        )
        market_cap = cls.calculate_market_cap(
            data.get("current_price", 0), data.get("weighted_average_shares_outstanding", 0)
        )
        net_current_asset_value = cls.calculate_net_current_asset_value(
            data.get("total_current_assets", 0),
            data.get("total_liabilities", 0),
            data.get("weighted_average_shares_outstanding", 0),
        )
        payout_ratio = cls.calculate_payout_ratio(
            data.get("dividends_paid", 0),
            data.get("net_income", 0),
        )
        tangible_assets = cls.calculate_tangible_assets(
            data.get("total_current_assets", 0),
            data.get("property_plant_equipment_net", 0),
        )
        retention_ratio = cls.calculate_retention_ratio(
            data.get("dividends_paid", 0),
            data.get("net_income", 0),
        )

        return {
            "normalized_income": normalized_income,
            "effective_tax_rate": effective_tax_rate,
            "net_working_capital": net_working_capital,
            "average_inventory": average_inventory,
            "average_accounts_payable": average_accounts_payable,
            "dividend_yield": dividend_yield,
            "earnings_yield": earnings_yield,
            "fcf_yield": fcf_yield,
            "income_quality": income_quality,
            "invested_capital": invested_capital,
            "market_cap": market_cap,
            "net_current_asset_value": net_current_asset_value,
            "payout_ratio": payout_ratio,
            "tangible_assets": tangible_assets,
            "retention_ratio": retention_ratio,
        }

    @classmethod
    def calculate_operation_risk_ratios(
        cls, data: Dict[str, Union[int, float]]
    ) -> Dict[str, Union[int, float]]:
        asset_coverage_ratio = cls.calculate_asset_coverage_ratio(
            data.get("total_assets", 0),
            data.get("goodwill_and_intangible_assets", 0),
            data.get("total_current_liabilities", 0),
            data.get("short_term_debt", 0),
            data.get("interest_expense", 0),
        )
        cash_flow_coverage_ratios = cls.calculate_cash_flow_coverage_ratios(
            data.get("net_cash_provided_by_operating_activities", 0),
            data.get("total_debt", 0),
        )
        cash_coverage = cls.calculate_cash_coverage(
            data.get("cash_and_short_term_investments", 0),
            data.get("interest_expense", 0),
        )
        debt_service_coverage = cls.calculate_debt_service_coverage(
            data.get("operating_income", 0),
            data.get("total_debt", 0),
        )
        interest_coverage = cls.calculate_interest_coverage(
            data.get("operating_income", 0),
            data.get("interest_expense", 0),
        )
        operating_cashflow_ratio = cls.calculate_operating_cashflow_ratio(
            data.get("net_cash_provided_by_operating_activities", 0),
            data.get("total_current_liabilities", 0),
        )
        debt_ratio = cls.calculate_debt_ratio(
            data.get("total_debt", 0),
            data.get("total_assets", 0),
        )
        long_term_debt_to_capitalization = cls.calculate_long_term_debt_to_capitalization(
            data.get("long_term_debt", 0),
            data.get("common_stock", 0),
        )
        total_debt_to_capitalization = cls.calculate_total_debt_to_capitalization(
            data.get("total_debt", 0),
            data.get("debt_and_equity", 0),
        )

        return {
            "asset_coverage_ratio": asset_coverage_ratio,
            "cash_flow_coverage_ratios": cash_flow_coverage_ratios,
            "cash_coverage": cash_coverage,
            "debt_service_coverage": debt_service_coverage,
            "interest_coverage": interest_coverage,
            "operating_cashflow_ratio": operating_cashflow_ratio,
            "debt_ratio": debt_ratio,
            "long_term_debt_to_capitalization": long_term_debt_to_capitalization,
            "total_debt_to_capitalization": total_debt_to_capitalization,
        }

    @classmethod
    def calculate_enterprise_value_ratios(
        cls, data: Dict[str, Union[int, float]]
    ) -> Dict[str, Union[int, float]]:
        market_cap = cls.calculate_market_cap(
            data.get("current_price", 0),
            data.get("weighted_average_shares_outstanding", 0),
        )
        enterprise_value = cls.calculate_enterprise_value(
            market_cap,
            data.get("total_debt", 0),
            data.get("cash_and_short_term_investments", 0),
        )
        ev_fcf = cls.calculate_ev_fcf(
            enterprise_value,
            data.get("free_cash_flow", 0),
        )
        ev_operating_cf = cls.calculate_ev_operating_cf(
            enterprise_value,
            data.get("net_cash_provided_by_operating_activities", 0),
        )
        ev_sales = cls.calculate_ev_sales(
            enterprise_value,
            data.get("revenue", 0),
        )
        company_equity_multiplier = cls.calculate_company_equity_multiplier(
            data.get("total_assets", 0),
            data.get("total_stockholders_equity", 0),
        )
        ev_multiple = cls.calculate_ev_multiple(
            enterprise_value,
            data.get("ebitda", 0),
        )

        return {
            "market_cap": market_cap,
            "enterprise_value": enterprise_value,
            "ev_fcf": ev_fcf,
            "ev_operating_cf": ev_operating_cf,
            "ev_sales": ev_sales,
            "company_equity_multiplier": company_equity_multiplier,
            "ev_multiple": ev_multiple,
        }

    @classmethod
    def calculate_company_growth(
        cls, data: Dict[str, Union[int, float]]
    ) -> Dict[str, Union[int, float]]:
        revenue_growth = cls.calculate_revenue_growth(
            data.get("revenue", 0),
            data.get("last_year_revenue", 0),
        )
        cost_revenue_growth = cls.calculate_cost_revenue_growth(
            data.get("cost_of_revenue", 0),
            data.get("last_year_cost_revenue", 0),
        )
        operating_expenses_growth = cls.calculate_operating_expenses_growth(
            data.get("cost_and_expenses", 0),
            data.get("last_year_cost_expense", 0),
        )
        net_income_growth = cls.calculate_net_income_growth(
            data.get("net_income", 0),
            data.get("last_year_net_income", 0),
        )
        shares_buyback = cls.calculate_shares_buyback(
            data.get("weighted_average_shares_outstanding", 0),
            data.get("last_year_shares_outstanding", 0),
        )
        eps_growth = cls.calculate_eps_growth(
            data.get("eps", 0),
            data.get("last_year_eps", 0),
        )
        fcf_growth = cls.calculate_fcf_growth(
            data.get("free_cash_flow", 0),
            data.get("last_year_fcf", 0),
        )
        owners_earnings_growth = cls.calculate_owners_earnings_growth(
            data.get("owners_earnings", 0),
            data.get("last_year_owner_earnings", 0),
        )
        capex_growth = cls.calculate_capex_growth(
            data.get("capital_expenditure", 0),
            data.get("last_year_capex", 0),
        )
        rd_expenses_growth = cls.calculate_rd_expenses_growth(
            data.get("rd_expenses", 0),
            data.get("last_year_research_dev", 0),
        )

        return {
            "revenue_growth": revenue_growth,
            "cost_revenue_growth": cost_revenue_growth,
            "operating_expenses_growth": operating_expenses_growth,
            "net_income_growth": net_income_growth,
            "shares_buyback": shares_buyback,
            "eps_growth": eps_growth,
            "fcf_growth": fcf_growth,
            "owners_earnings_growth": owners_earnings_growth,
            "capex_growth": capex_growth,
            "rd_expenses_growth": rd_expenses_growth,
        }

    @classmethod
    def calculate_efficiency_ratios(
        cls, data: Dict[str, Union[int, float]]
    ) -> Dict[str, Union[int, float]]:
        days_inventory_outstanding = cls.calculate_days_inventory_outstanding(
            data.get("average_inventory", 0),
            data.get("cost_of_revenue", 0),
        )
        days_payables_outstanding = cls.calculate_days_payable_outstanding(
            data.get("accounts_payable", 0),
            data.get("cost_of_goods_sold", 0),
        )
        days_sales_outstanding = cls.calculate_days_sales_outstanding(
            data.get("accounts_receivable", 0),
            data.get("accounts_payable", 0),
        )
        operating_cycle = cls.calculate_operating_cycle(
            days_inventory_outstanding, days_sales_outstanding
        )
        cash_conversion_cycle = cls.calculate_cash_conversion_cycle(
            days_inventory_outstanding,
            days_sales_outstanding,
            days_payables_outstanding,
        )
        asset_turnover = cls.calculate_asset_turnover(
            data.get("revenue", 0),
            data.get("average_assets", 0),
        )
        inventory_turnover = cls.calculate_inventory_turnover(
            data.get("cost_of_revenue", 0),
            data.get("average_inventory", 0),
        )
        fixed_asset_turnover = cls.calculate_fixed_asset_turnover(
            data.get("revenue", 0),
            data.get("average_fixed_assets", 0),
        )
        accounts_payable_turnover = cls.calculate_accounts_payable_turnover(
            data.get("accounts_payable", 0),
            data.get("average_accounts_payable", 0),
        )
        free_cashflow_to_operating_cashflow = (
            cls.calculate_free_cashflow_to_operating_cashflow(
                data.get("free_cash_flow", 0),
                data.get("net_cash_provided_by_operating_activities", 0),
            )
        )
        return {
            "days_inventory_outstanding": days_inventory_outstanding,
            "days_payables_outstanding": days_payables_outstanding,
            "days_sales_outstanding": days_sales_outstanding,
            "operating_cycle": operating_cycle,
            "cash_conversion_cycle": cash_conversion_cycle,
            "asset_turnover": asset_turnover,
            "inventory_turnover": inventory_turnover,
            "fixed_asset_turnover": fixed_asset_turnover,
            "accounts_payable_turnover": accounts_payable_turnover,
            "free_cashflow_to_operating_cashflow": free_cashflow_to_operating_cashflow,
        }

    @classmethod
    def calculate_price_to_ratios(
        cls, data: Dict[str, Union[int, float]]
    ) -> Dict[str, Union[int, float]]:
        price_to_book = cls.calculate_price_to_book(
            data.get("current_price", 0),
            data.get("book_ps", 0),
        )
        price_to_cf = cls.calculate_price_to_cash(
            data.get("current_price", 0),
            data.get("cash_ps", 0),
        )
        price_to_earnings = cls.calculate_price_to_earnings(
            data.get("current_price", 0),
            data.get("eps", 0),
        )
        price_to_earnings_growth = cls.calculate_price_to_earnings_growth(
            price_to_earnings, data.get("net_income_growth", 0)
        ).real
        price_to_sales = cls.calculate_price_to_sales(
            data.get("current_price", 0),
            data.get("sales_ps", 0),
        )
        price_to_total_assets = cls.calculate_price_to_total_assets(
            data.get("current_price", 0),
            data.get("total_assets_ps", 0),
        )
        price_to_fcf = cls.calculate_price_to_fcf(
            data.get("current_price", 0),
            data.get("fcf_ps", 0),
        )
        price_to_operating_cf = cls.calculate_price_to_operating_cf(
            data.get("current_price", 0),
            data.get("operating_cf_ps", 0),
        )
        price_to_tangible_assets = cls.calculate_price_to_tangible_assets(
            data.get("current_price", 0),
            data.get("tangible_ps", 0),
        )
        return {
            "price_book": price_to_book,
            "price_cf": price_to_cf,
            "price_earnings": price_to_earnings,
            "price_earnings_growth": price_to_earnings_growth,
            "price_sales": price_to_sales,
            "price_total_assets": price_to_total_assets,
            "price_fcf": price_to_fcf,
            "price_operating_cf": price_to_operating_cf,
            "price_tangible_assets": price_to_tangible_assets,
        }

    @classmethod
    def calculate_all_ratios(
        cls,
        current_income_statements: Union[List, QuerySet],
        current_balance_sheets: Union[List, QuerySet],
        current_cashflow_statements: Union[List, QuerySet],
        previous_income_statements: Union[List, QuerySet],
        previous_balance_sheets: Union[List, QuerySet],
        previous_cashflow_statements: Union[List, QuerySet],
        current_price: Dict[str, Union[int, float]],
    ) -> Dict[str, Dict[str, Union[int, float]]]:
        base_data = cls.prepare_base_data(
            current_income_statements,
            current_balance_sheets,
            current_cashflow_statements,
            previous_income_statements,
            previous_balance_sheets,
            previous_cashflow_statements,
            current_price,
        )

        other_ratios = cls.calculate_other_ratios(base_data)
        base_data.update(other_ratios)

        fcf_ratio = cls.calculate_free_cashflow_ratios(base_data)
        base_data.update(fcf_ratio)

        ps_value = cls.calculate_per_share_value(base_data)
        base_data.update(ps_value)

        company_growth = cls.calculate_company_growth(base_data)
        base_data.update(company_growth)

        non_gaap = cls.calculate_non_gaap(base_data)
        base_data.update(non_gaap)

        return {
            "price_to_ratio": cls.calculate_price_to_ratios(base_data),
            "efficiency_ratio": cls.calculate_efficiency_ratios(base_data),
            "enterprise_value_ratio": cls.calculate_enterprise_value_ratios(base_data),
            "liquidity_ratio": cls.calculate_liquidity_ratios(base_data),
            "margin_ratio": cls.calculate_margin_ratios(base_data),
            "operation_risk_ratio": cls.calculate_operation_risk_ratios(base_data),
            "rentability_ratios": cls.calculate_rentability_ratios(base_data),
            "fcf_ratio": fcf_ratio,
            "ps_value": ps_value,
            "company_growth": company_growth,
            "non_gaap": non_gaap,
            "other_ratios": other_ratios,
            "current_price": current_price,
        }
