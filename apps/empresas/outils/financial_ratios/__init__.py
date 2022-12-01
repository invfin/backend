from typing import Dict, Union

from .valuation_ratios import ValuationRatios
from .efficiency_ratios import EfficiencyRatios
from .liquidity_ratios import LiquidityRatios
from .operation_risk_ratios import OperationRiskRatios
from .per_share_values import PerShareValues
from .rentability_ratios import RentabilityRatios
from .margins import Margins
from .free_cashflow_ratios import FreeCashFlowRatios

class CalculateFinancialRatios(
    ValuationRatios,
    EfficiencyRatios,
    LiquidityRatios,
    OperationRiskRatios,
    PerShareValues,
    RentabilityRatios,
    Margins,
    FreeCashFlowRatios,
):
    def generate_current_data(
        self, income_statements: list, balance_sheets: list, cashflow_statements: list
    ) -> Dict[str, Union[int, float]]:
        current_data = {}
        current_price = self.get_most_recent_price()
        current_income_statements = income_statements[0]
        current_balance_sheets = balance_sheets[0]
        current_cashflow_statements = cashflow_statements[0]
        current_fecha = {
            "date": current_income_statements["calendarYear"],
            "year": current_income_statements["date"],
        }
        current_data.update(current_price)
        current_data.update(current_income_statements)
        current_data.update(current_balance_sheets)
        current_data.update(current_cashflow_statements)
        current_data.update(current_fecha)

        return current_data

    def generate_last_year_data(
        self, income_statements: list, balance_sheets: list, cashflow_statements: list
    ) -> Dict[str, Union[int, float]]:
        ly_data = {}
        ly_income_statements = income_statements[1]
        ly_balance_sheets = balance_sheets[1]
        ly_cashflow_statements = cashflow_statements[1]
        ly_fecha = {
            "date": ly_income_statements["calendarYear"],
            "year": ly_income_statements["date"],
        }
        ly_data.update(ly_income_statements)
        ly_data.update(ly_balance_sheets)
        ly_data.update(ly_cashflow_statements)
        ly_data.update(ly_fecha)

        return self.last_year_data(ly_data)

    def calculate_all_ratios(
        self, income_statements: list, balance_sheets: list, cashflow_statements: list
    ) -> Dict[str, Dict[str, Union[int, float]]]:
        current_data = self.generate_current_data(income_statements, balance_sheets, cashflow_statements)
        ly_data = self.generate_last_year_data(income_statements, balance_sheets, cashflow_statements)

        all_data = current_data
        all_data.update(ly_data)

        main_ratios = self.calculate_main_ratios(all_data)
        all_data.update(main_ratios)

        fcf_ratio = self.calculate_fcf_ratios(current_data)
        all_data.update(fcf_ratio)

        ps_value = self.calculate_ps_value(all_data)
        all_data.update(ps_value)

        company_growth = self.calculate_company_growth(all_data)
        all_data.update(company_growth)

        non_gaap = self.calculate_non_gaap(all_data)
        all_data.update(non_gaap)

        price_to_ratio = self.calculate_price_to_ratios(all_data)
        eficiency_ratio = self.calculate_efficiency_ratios(all_data)
        enterprise_value_ratio = self.calculate_enterprise_value_ratios(all_data)
        liquidity_ratio = self.calculate_liquidity_ratios(all_data)
        margin_ratio = self.calculate_margin_ratios(all_data)
        operation_risk_ratio = self.calculate_operation_risk_ratios(all_data)
        rentability_ratios = self.calculate_rentability_ratios(all_data)

        return {
            "current_data": current_data,
            "price_to_ratio": price_to_ratio,
            "eficiency_ratio": eficiency_ratio,
            "enterprise_value_ratio": enterprise_value_ratio,
            "liquidity_ratio": liquidity_ratio,
            "margin_ratio": margin_ratio,
            "operation_risk_ratio": operation_risk_ratio,
            "rentability_ratios": rentability_ratios,
            "fcf_ratio": fcf_ratio,
            "ps_value": ps_value,
            "company_growth": company_growth,
            "non_gaap": non_gaap,
            "main_ratios": main_ratios,
        }

    def last_year_data(self, data: Dict[str, Union[int, float]]) -> Dict[str, Union[int, float]]:
        last_year_inventory = data["inventory"]
        last_year_accounts_payable = data["account_payables"]
        last_year_revenue = data["revenue"]
        last_year_net_income = data["net_income"]
        last_year_fcf = data["free_cash_flow"]
        last_year_capex = data["capital_expenditure"]
        last_year_shares_outstanding = data["weighted_average_shares_out"]
        last_year_cost_expense = data["cost_and_expenses"]  # TODO check what is this cost of expenses
        last_year_cost_revenue = data["cost_of_revenue"]
        last_year_eps = (
            data["net_income"] / data["weighted_average_shares_out"] if data["weighted_average_shares_out"] != 0 else 0
        )
        last_year_research_dev = data["rd_expenses"]
        last_year_fixed_assets = data["property_plant_equipment_net"]
        last_year_assets = data["total_assets"]
        last_year_owner_earnings = (
            data["net_income"]
            + data["depreciation_and_amortization"]
            + data["change_in_working_capital"]
            + data["capital_expenditure"]
        )
        last_year_current_assets = data["total_current_assets"]
        last_year_current_liabilities = data["total_current_liabilities"]

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

    def calculate_main_ratios(self, data: Dict[str, Union[int, float]]) -> Dict[str, Union[int, float]]:
        average_fixed_assets = (data["last_year_fixed_assets"] + data["property_plant_equipment_net"]) / 2
        average_assets = (data["last_year_assets"] + data["total_assets"]) / 2
        net_working_capital = data["total_current_assets"] - data["total_current_liabilities"]
        change_in_working_capital = net_working_capital - (
            data["last_year_current_assets"] - data["last_year_current_liabilities"]
        )
        gross_invested_capital = (
            net_working_capital + data["property_plant_equipment_net"] + data["depreciation_and_amortization"]
        )
        effective_tax_rate = (
            (data["income_tax_expense"] / data["operating_income"]) if data["operating_income"] != 0 else 0
        )
        net_tangible_equity = (data["total_current_assets"] + data["property_plant_equipment_net"]) - data[
            "total_liabilities"
        ]
        nopat = (
            data["operating_income"] * (1 - (data["income_tax_expense"] / data["operating_income"]))
            if data["operating_income"] != 0
            else 0
        )
        debt_and_equity = data["total_debt"] + data["total_stockholders_equity"]
        non_cash_workcap = net_working_capital - data["cash_and_cash_equivalents"]
        invested_capital = data["property_plant_equipment_net"] + non_cash_workcap

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
            "non_cash_workcap": non_cash_workcap,
            "invested_capital": invested_capital,
        }

    @classmethod
    def calculate_rentability_ratios(cls, data: Dict[str, Union[int, float]]) -> Dict[str, Union[int, float]]:
        capital_employed = data["total_assets"] - data["total_current_liabilities"]
        roa = cls.calculate_roa(data.get("net_income", 0), data.get("total_assets", 0))
        roe = cls.calculate_roe(data.get("net_income", 0), data.get("total_stockholders_equity", 0))
        roc = cls.calculate_roc(data.get("operating_income", 0), data.get("total_assets", 0))
        roce = cls.calculate_roce(data.get("operating_income", 0), data.get("capital_employed", 0))
        rota = cls.calculate_rota(data.get("net_income", 0), data.get("tangible_assets", 0))
        roic = cls.calculate_roic(data.get("net_income", 0), data.get("dividends_paid", 0), data.get("invested_capital", 0),)
        nopat_roic = cls.calculate_nopat_roic(data.get("nopat", 0), data.get("invested_capital", 0))
        rogic = cls.calculate_rogic(data.get("nopat", 0), data.get("gross_invested_capital", 0))
        return {
            "roa": roa,
            "roe": roe,
            "roc": roc,
            "roce": roce,
            "rota": rota,
            "roic": roic,
            "nopat_roic": nopat_roic,
            "rogic": rogic,
        }

    @classmethod
    def calculate_liquidity_ratios(cls, data: Dict[str, Union[int, float]]) -> Dict[str, Union[int, float]]:
        cash_ratio = cls.calculate_cash_ratio(
            data.get("cash_and_cash_equivalents",0), data.get("total_current_liabilities",0)
        )
        current_ratio = cls.calculate_current_ratio(
            data.get("total_current_assets",0) , data.get("total_current_liabilities",0)
        )
        quick_ratio = cls.calculate_quick_ratio(
            data.get("net_receivables",0) , data.get("cash_and_short_term_investments",0), data.get("total_current_liabilities",0)
        )
        operating_cashflow_ratio = cls.calculate_operating_cashflow_ratio(
            data.get("net_cash_provided_by_operating_activities",0) , data.get("total_current_liabilities",0)
        )
        debt_to_equity = cls.calculate_debt_to_equity(
            data.get("total_liabilities",0) , data.get("total_stockholders_equity",0)
        )

        return {
            "cash_ratio": cash_ratio,
            "current_ratio": current_ratio,
            "quick_ratio": quick_ratio,
            "operating_cashflow_ratio": operating_cashflow_ratio,
            "debt_to_equity": debt_to_equity,
        }

    @classmethod
    def calculate_margin_ratios(cls, data: Dict[str, Union[int, float]]) -> Dict[str, Union[int, float]]:
        gross_margin = cls.calculate_gross_margin(data.get("gross_profit", 0) , data.get("revenue",0))
        ebitda_margin = cls.calculate_ebitda_margin(data.get("ebitda", 0) , data.get("revenue",0))
        net_income_margin = cls.calculate_net_income_margin(data.get("net_income", 0) , data.get("revenue",0))
        fcf_margin = cls.calculate_fcf_margin(data.get("free_cash_flow", 0) , data.get("revenue",0))
        fcf_equity_to_net_income = cls.calculate_fcf_equity_to_net_income(data.get("fcf_equity", 0) , data.get("net_income",0))
        unlevered_fcf_to_net_income = cls.calculate_unlevered_fcf_to_net_income(data.get("unlevered_fcf", 0) , data.get("net_income",0))
        unlevered_fcf_ebit_to_net_income = cls.calculate_unlevered_fcf_ebit_to_net_income(
            data.get("unlevered_fcf_ebit",0) , data.get("net_income",0)
        )
        owners_earnings_to_net_income = cls.calculate_owners_earnings_to_net_income(
            data.get("owners_earnings",0) , data.get("net_income",0)
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
    def calculate_fcf_ratios(cls, data: Dict[str, Union[int, float]]) -> Dict[str, Union[int, float]]:
        fcf_equity = cls.calculate_fcf_equity(data.get("net_cash_provided_by_operating_activities",0) , data.get("capital_expenditure",0) , data.get("debt_repayment",0))
        unlevered_fcf = cls.calculate_unlevered_fcf(
            data.get("nopat", 0)
            ,data.get("depreciation_and_amortization", 0)
            ,data.get("change_in_working_capital", 0)
            ,data.get("capital_expenditure", 0)
        )
        unlevered_fcf_ebit = cls.calculate_unlevered_fcf_ebit(
            data.get("operating_income", 0)
            ,data.get("depreciation_and_amortization", 0)
            ,data.get("deferred_income_tax", 0)
            ,data.get("change_in_working_capital", 0)
            ,data.get("capital_expenditure", 0)
        )
        owners_earnings = cls.calculate_owners_earnings(
            data.get("net_income", 0)
            ,data.get("depreciation_and_amortization", 0)
            ,data.get("change_in_working_capital", 0)
            ,data.get("capital_expenditure", 0)
        )

        return {
            "fcf_equity": fcf_equity,
            "unlevered_fcf": unlevered_fcf,
            "unlevered_fcf_ebit": unlevered_fcf_ebit,
            "owners_earnings": owners_earnings,
        }

    @classmethod
    def calculate_ps_value(cls, data: Dict[str, Union[int, float]]) -> Dict[str, Union[int, float]]:
        sales_ps = cls.calculate_sales_ps(
            data.get("revenue",0) , data.get("weighted_average_shares_out",0),
        )
        book_ps = cls.calculate_book_ps(
            data.get("total_stockholders_equity",0) , data.get("weighted_average_shares_out",0),
        )
        tangible_ps = cls.calculate_tangible_ps(
            data.get("net_tangible_equity",0) , data.get("weighted_average_shares_out",0),
        )
        fcf_ps = cls.calculate_fcf_ps(
            data.get("free_cash_flow",0) , data.get("weighted_average_shares_out",0),
        )
        eps = cls.calculate_eps(
            data.get("net_income",0) , data.get("weighted_average_shares_out",0),
        )
        cash_ps = cls.calculate_cash_ps(
            data.get("cash_and_short_term_investments",0) , data.get("weighted_average_shares_out",0),
        )
        operating_cf_ps = cls.calculate_operating_cf_ps(
            data.get("net_cash_provided_by_operating_activities",0) , data.get("weighted_average_shares_out",0),
        )
        capex_ps = cls.calculate_capex_ps(
            data.get("capital_expenditure",0) , data.get("weighted_average_shares_out",0),
        )
        total_assets_ps = cls.calculate_total_assets_ps(
            data.get("total_assets",0) , data.get("weighted_average_shares_out",0),
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

    def calculate_non_gaap(self, data: Dict[str, Union[int, float]]) -> Dict[str, Union[int, float]]:
        normalized_income = data["net_income"] - data["total_other_income_expenses_net"]
        effective_tax_rate = (
            (data["income_tax_expense"] / data["operating_income"]) if data["operating_income"] != 0 else 0
        )
        nopat = data["nopat"]
        net_working_cap = data["total_current_assets"] - data["total_current_liabilities"]
        average_inventory = (data["last_year_inventory"] + data["inventory"]) / 2
        average_payables = (data["last_year_accounts_payable"] + data["account_payables"]) / 2
        divs_per_share = data["dividends_paid"] / data["common_stock"] if data["common_stock"] != 0 else 0
        dividend_yield = divs_per_share / data["current_price"] if data["current_price"] != 0 else 0
        earnings_yield = (data["eps"] / data["current_price"]) * 100 if data["current_price"] != 0 else 0
        fcf_yield = (data["fcf_ps"] / data["current_price"]) * 100 if data["current_price"] != 0 else 0
        income_quality = (
            (data["net_cash_provided_by_operating_activities"] / data["net_income"]) * 100 if data["net_income"] != 0 else 0
        )
        invested_capital = (
            data["property_plant_equipment_net"] + data["net_working_capital"] - data["cash_and_cash_equivalents"]
        )
        market_cap = data["current_price"] * data["weighted_average_shares_out"]
        net_current_asset_value = (
            (data["total_current_assets"] - (data["total_liabilities"])) / data["weighted_average_shares_out"]
            if data["weighted_average_shares_out"] != 0
            else 0
        )
        payout_ratio = abs(data["dividends_paid"] / data["net_income"]) * 100 if data["net_income"] != 0 else 0
        tangible_assets = data["total_current_assets"] + data["property_plant_equipment_net"]
        retention_ratio = 100 - (
            abs(data["dividends_paid"] / data["net_income"]) * 100 if data["net_income"] != 0 else 0
        )

        return {
            "normalized_income": normalized_income,
            "effective_tax_rate": effective_tax_rate,
            "nopat": nopat,
            "net_working_cap": net_working_cap,
            "average_inventory": average_inventory,
            "average_payables": average_payables,
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
    def calculate_operation_risk_ratios(cls, data: Dict[str, Union[int, float]]) -> Dict[str, Union[int, float]]:
        asset_coverage_ratio = cls.calculate_asset_coverage_ratio(
                data.get("total_assets", 0),
                data.get("goodwill_and_intangible_assets", 0),
                data.get("total_current_liabilities", 0),
                data.get("short_term_debt", 0),
                data.get("interest_expense", 0),
            )
        cash_flow_coverage_ratios = cls.calculate_cash_flow_coverage_ratios(
            data.get("net_cash_provided_by_operating_activities",0) , data.get("total_debt",0),
        )
        cash_coverage = cls.calculate_cash_coverage(
            data.get("cash_and_short_term_investments",0) , data.get("interest_expense",0),
        )
        debt_service_coverage = cls.calculate_debt_service_coverage(data.get("operating_income",0) , data.get("total_debt",0),)
        interest_coverage = cls.calculate_interest_coverage(data.get("operating_income",0) , data.get("interest_expense",0),)
        operating_cashflow_ratio = cls.calculate_operating_cashflow_ratio(
            data.get("net_cash_provided_by_operating_activities", 0) , data.get("total_current_liabilities",0),

        )
        debt_ratio = cls.calculate_debt_ratio(data.get("total_debt",0) , data.get("total_assets",0))
        long_term_debt_to_capitalization = cls.calculate_long_term_debt_to_capitalization(data.get("long_term_debt",0), data.get("common_stock", 0),)
        total_debt_to_capitalization = cls.calculate_total_debt_to_capitalization(data.get("total_debt",0) , data.get("debt_and_equity",0),)

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

    def calculate_enterprise_value_ratios(self, data: Dict[str, Union[int, float]]) -> Dict[str, Union[int, float]]:
        market_cap = data["current_price"] * data["weighted_average_shares_out"]
        enterprise_value = market_cap + data["total_debt"] - data["cash_and_short_term_investments"]
        ev_fcf = enterprise_value / data["free_cash_flow"] if data["free_cash_flow"] != 0 else 0
        ev_operating_cf = (
            enterprise_value / data["net_cash_provided_by_operating_activities"]
            if data["net_cash_provided_by_operating_activities"] != 0
            else 0
        )
        ev_sales = enterprise_value / data["revenue"] if data["revenue"] != 0 else 0
        company_equity_multiplier = (
            data["total_assets"] / data["total_stockholders_equity"] if data["total_stockholders_equity"] != 0 else 0
        )
        ev_multiple = enterprise_value / data["ebitda"] if data["ebitda"] != 0 else 0

        return {
            "market_cap": market_cap,
            "enterprise_value": enterprise_value,
            "ev_fcf": ev_fcf,
            "ev_operating_cf": ev_operating_cf,
            "ev_sales": ev_sales,
            "company_equity_multiplier": company_equity_multiplier,
            "ev_multiple": ev_multiple,
        }

    def calculate_company_growth(self, data: Dict[str, Union[int, float]]) -> Dict[str, Union[int, float]]:
        revenue_growth = (
            (data["revenue"] - data["last_year_revenue"]) / data["last_year_revenue"]
            if data["last_year_revenue"] != 0
            else 0
        )
        cost_revenue_growth = (
            (data["cost_of_revenue"] - data["last_year_cost_revenue"]) / data["last_year_cost_revenue"]
            if data["last_year_cost_revenue"] != 0
            else 0
        )
        operating_expenses_growth = (
            (data["cost_and_expenses"] - data["last_year_cost_expense"]) / data["last_year_cost_expense"]
            if data["last_year_cost_expense"] != 0
            else 0
        )
        net_income_growth = (
            (data["net_income"] - data["last_year_net_income"]) / data["last_year_net_income"]
            if data["last_year_net_income"] != 0
            else 0
        )
        shares_buyback = (
            (data["weighted_average_shares_out"] - data["last_year_shares_outstanding"])
            / data["last_year_shares_outstanding"]
            if data["last_year_shares_outstanding"] != 0
            else 0
        )
        eps_growth = (data["eps"] - data["last_year_eps"]) / data["last_year_eps"] if data["last_year_eps"] != 0 else 0
        fcf_growth = (
            (data["free_cash_flow"] - data["last_year_fcf"]) / data["last_year_fcf"]
            if data["last_year_fcf"] != 0
            else 0
        )
        owners_earnings_growth = (
            (data["owners_earnings"] - data["last_year_owner_earnings"]) / data["last_year_owner_earnings"]
            if data["last_year_owner_earnings"] != 0
            else 0
        )
        capex_growth = (
            (data["capital_expenditure"] - data["last_year_capex"]) / data["last_year_capex"]
            if data["last_year_capex"] != 0
            else 0
        )
        rd_expenses_growth = (
            (data["rd_expenses"] - data["last_year_research_dev"]) / data["last_year_research_dev"]
            if data["last_year_research_dev"] != 0
            else 0
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
    def calculate_average_inventory(cls, data: Dict[str, Union[int, float]]) -> Union[int, float]:
        return (data["last_year_inventory"] + data["inventory"]) / 2

    @classmethod
    def calculate_efficiency_ratios(cls, data: Dict[str, Union[int, float]]) -> Dict[str, Union[int, float]]:
        average_inventory = data.get("average_inventory", cls.calculate_average_inventory(data))
        days_inventory_outstanding = cls.calculate_days_inventory_outstanding(average_inventory, data.get("cost_of_revenue",0),)
        days_payables_outstanding = cls.calculate_days_payables_outstanding(data.get("account_payables",0), data.get("cost_of_goods_sold",0),)
        days_sales_outstanding = cls.calculate_days_sales_outstanding(data.get("accounts_receivables",0), data.get("account_payables",0),)
        operating_cycle = cls.calculate_operating_cycle(days_inventory_outstanding, days_sales_outstanding)
        cash_conversion_cycle = cls.calculate_cash_conversion_cycle(days_inventory_outstanding, days_sales_outstanding, days_payables_outstanding,)
        asset_turnover = cls.calculate_asset_turnover(data.get("revenue", 0), data.get("average_assets", 0))
        inventory_turnover = cls.calculate_inventory_turnover(data.get("cost_of_revenue", 0), average_inventory)
        fixed_asset_turnover = cls.calculate_fixed_asset_turnover(data.get("revenue", 0), data.get("average_fixed_assets", 0),)
        payables_turnover = cls.calculate_payables_turnover(data.get("account_payables", 0), data.get("average_payables", 0),)
        fcf_to_operating_cf = cls.calculate_fcf_to_operating_cf(data.get("free_cash_flow", 0), data.get("net_cash_provided_by_operating_activities", 0),)
        return {
            "days_inventory_outstanding": days_inventory_outstanding,
            "days_payables_outstanding": days_payables_outstanding,
            "days_sales_outstanding": days_sales_outstanding,
            "operating_cycle": operating_cycle,
            "cash_conversion_cycle": cash_conversion_cycle,
            "asset_turnover": asset_turnover,
            "inventory_turnover": inventory_turnover,
            "fixed_asset_turnover": fixed_asset_turnover,
            "payables_turnover": payables_turnover,
            "fcf_to_operating_cf": fcf_to_operating_cf,
        }

    @classmethod
    def calculate_price_to_ratios(cls, data: Dict[str, Union[int, float]]) -> Dict[str, Union[int, float]]:
        price_to_book = cls.calculate_price_to_book(data.get("current_price",0), data.get("book_ps",0))
        price_to_cf = cls.calculate_price_to_cash(data.get("current_price",0), data.get("cash_ps",0))
        price_to_earnings = cls.calculate_price_to_earnings(data.get("current_price",0), data.get("eps",0))
        price_to_earnings_growth = cls.calculate_price_to_earnings_growth(price_to_earnings, data.get("net_income_growth",0)).real
        price_to_sales = cls.calculate_price_to_sales(data.get("current_price",0), data.get("sales_ps",0))
        price_to_total_assets = cls.calculate_price_to_total_assets(data.get("current_price",0), data.get("total_assets_ps",0))
        price_to_fcf = cls.calculate_price_to_fcf(data.get("current_price",0), data.get("fcf_ps",0))
        price_to_operating_cf = cls.calculate_price_to_operating_cf(data.get("current_price",0), data.get("operating_cf_ps",0))
        price_to_tangible_assets = cls.calculate_price_to_tangible_assets(data.get("current_price",0), data.get("tangible_ps",0))
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
