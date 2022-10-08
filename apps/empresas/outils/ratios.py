from decimal import Decimal
from typing import Dict, Union


class CalculateCompanyFinancialRatios:
    @staticmethod
    def divide_or_zero(numerator: Union[int, float], denominator: Union[int, float]):
        """Function to make a division even if it may return zero

        Args:
            numerator: (Union[int, float])
                The numerator of the division
            denominator (Union[int, float]):
                The denominator of the division

        """

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
    ) -> Dict[str, Union[int, float]]:
        current_data = self.generate_current_data(income_statements, balance_sheets, cashflow_statements)
        ly_data = self.generate_last_year_data(income_statements, balance_sheets, cashflow_statements)

        all_data = current_data
        all_data.update(ly_data)

        main_ratios = self.calculate_main_ratios(all_data)
        all_data.update(main_ratios)

        fcf_ratio = self.calculate_fcf_ratio(current_data)
        all_data.update(fcf_ratio)

        ps_value = self.calculate_ps_value(all_data)
        all_data.update(ps_value)

        company_growth = self.calculate_company_growth(all_data)
        all_data.update(company_growth)

        non_gaap = self.calculate_non_gaap(all_data)
        all_data.update(non_gaap)

        price_to_ratio = self.calculate_price_to_ratio(all_data)
        eficiency_ratio = self.calculate_eficiency_ratio(all_data)
        enterprise_value_ratio = self.calculate_enterprise_value_ratio(all_data)
        liquidity_ratio = self.calculate_liquidity_ratio(all_data)
        margin_ratio = self.calculate_margin_ratio(all_data)
        operation_risk_ratio = self.calculate_operation_risk_ratio(all_data)
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
        last_year_cost_expense = data["costAndExpenses"]  # TODO check what is this cost of expenses
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
        averageFxAs = (data["last_year_fixed_assets"] + data["property_plant_equipment_net"]) / 2
        averageAsssets = (data["last_year_assets"] + data["total_assets"]) / 2
        netWorkingCapital = data["total_current_assets"] - data["total_current_liabilities"]
        changeInWorkingCap = netWorkingCapital - (
            data["last_year_current_assets"] - data["last_year_current_liabilities"]
        )
        grossInvestedCapital = (
            netWorkingCapital + data["property_plant_equipment_net"] + data["depreciation_and_amortization"]
        )
        effectiveTaxRate = (
            (data["income_tax_expense"] / data["operating_income"]) if data["operating_income"] != 0 else 0
        )
        netTangibleEquity = (data["total_current_assets"] + data["property_plant_equipment_net"]) - data[
            "totalLiabilities"
        ]
        nopat = (
            data["operating_income"] * (1 - (data["income_tax_expense"] / data["operating_income"]))
            if data["operating_income"] != 0
            else 0
        )
        debtAndEquity = data["total_debt"] + data["total_stockholders_equity"]
        non_cash_workcap = netWorkingCapital - data["cash_and_cash_equivalents"]
        investedCapital = data["property_plant_equipment_net"] + non_cash_workcap

        return {
            "averageFxAs": averageFxAs,
            "averageAsssets": averageAsssets,
            "netWorkingCapital": netWorkingCapital,
            "changeInWorkingCap": changeInWorkingCap,
            "grossInvestedCapital": grossInvestedCapital,
            "effectiveTaxRate": effectiveTaxRate,
            "netTangibleEquity": netTangibleEquity,
            "nopat": nopat,
            "debtAndEquity": debtAndEquity,
            "non_cash_workcap": non_cash_workcap,
            "investedCapital": investedCapital,
        }

    def calculate_rentability_ratios(self, data: Dict[str, Union[int, float]]) -> Dict[str, Union[int, float]]:
        capitalEmployed = data["total_assets"] - data["total_current_liabilities"]
        roa = (data["net_income"] / data["total_assets"]) * 100 if data["total_assets"] != 0 else 0
        roe = (
            (data["net_income"] / data["total_stockholders_equity"]) * 100
            if data["total_stockholders_equity"] != 0
            else 0
        )
        roc = (data["operating_income"] / data["total_assets"]) * 100 if data["total_assets"] != 0 else 0
        roce = (data["operating_income"] / capitalEmployed) * 100 if capitalEmployed != 0 else 0
        rota = (data["net_income"] / data["tangible_assets"]) * 100 if data["tangible_assets"] != 0 else 0
        roic = (
            ((data["net_income"] - data["dividendsPaid"]) / data["investedCapital"]) * 100
            if data["investedCapital"] != 0
            else 0
        )
        nopat_roic = (data["nopat"] / data["investedCapital"]) * 100 if data["investedCapital"] != 0 else 0
        rogic = (data["nopat"] / data["grossInvestedCapital"]) * 100 if data["grossInvestedCapital"] != 0 else 0

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

    def calculate_liquidity_ratio(self, data: Dict[str, Union[int, float]]) -> Dict[str, Union[int, float]]:
        cash_ratio = (
            data["cash_and_cash_equivalents"] / data["total_current_liabilities"]
            if data["total_current_liabilities"] != 0
            else 0
        )
        current_ratio = (
            data["total_current_assets"] / data["total_current_liabilities"]
            if data["total_current_liabilities"] != 0
            else 0
        )
        quick_ratio = (
            (data["netReceivables"] + data["cashAndShortTermInvestments"]) / data["total_current_liabilities"]
            if data["total_current_liabilities"] != 0
            else 0
        )
        operating_cashflow_ratio = (
            data["netCashProvidedByOperatingActivities"] / data["total_current_liabilities"]
            if data["total_current_liabilities"] != 0
            else 0
        )
        debt_to_equity = (
            data["totalLiabilities"] / data["total_stockholders_equity"]
            if data["total_stockholders_equity"] != 0
            else 0
        )

        return {
            "cash_ratio": cash_ratio,
            "current_ratio": current_ratio,
            "quick_ratio": quick_ratio,
            "operating_cashflow_ratio": operating_cashflow_ratio,
            "debt_to_equity": debt_to_equity,
        }

    def calculate_margin_ratio(self, data: Dict[str, Union[int, float]]) -> Dict[str, Union[int, float]]:
        gross_margin = data["grossProfit"] / data["revenue"] * 100 if data["revenue"] != 0 else 0
        ebitda_margin = data["ebitda"] / data["revenue"] * 100 if data["revenue"] != 0 else 0
        net_income_margin = data["net_income"] / data["revenue"] * 100 if data["revenue"] != 0 else 0
        fcf_margin = data["free_cash_flow"] / data["revenue"] * 100 if data["revenue"] != 0 else 0
        fcf_equity_to_net_income = data["fcf_equity"] / data["net_income"] * 100 if data["net_income"] != 0 else 0
        unlevered_fcf_to_net_income = data["unlevered_fcf"] / data["net_income"] * 100 if data["net_income"] != 0 else 0
        unlevered_fcf_ebit_to_net_income = (
            data["unlevered_fcf_ebit"] / data["net_income"] * 100 if data["net_income"] != 0 else 0
        )
        owners_earnings_to_net_income = (
            data["owners_earnings"] / data["net_income"] * 100 if data["net_income"] != 0 else 0
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

    def calculate_fcf_ratio(self, data: Dict[str, Union[int, float]]) -> Dict[str, Union[int, float]]:
        fcf_equity = data["netCashProvidedByOperatingActivities"] + data["capital_expenditure"] + data["debtRepayment"]
        unlevered_fcf = (
            data["nopat"]
            + data["depreciation_and_amortization"]
            + data["change_in_working_capital"]
            + data["capital_expenditure"]
        )
        unlevered_fcf_ebit = (
            data["operating_income"]
            + data["depreciation_and_amortization"]
            + data["deferredIncomeTax"]
            + data["change_in_working_capital"]
            + data["capital_expenditure"]
        )
        owners_earnings = (
            data["net_income"]
            + data["depreciation_and_amortization"]
            + data["change_in_working_capital"]
            + data["capital_expenditure"]
        )

        return {
            "fcf_equity": fcf_equity,
            "unlevered_fcf": unlevered_fcf,
            "unlevered_fcf_ebit": unlevered_fcf_ebit,
            "owners_earnings": owners_earnings,
        }

    def calculate_ps_value(self, data: Dict[str, Union[int, float]]) -> Dict[str, Union[int, float]]:
        sales_ps = (
            data["revenue"] / data["weighted_average_shares_out"] if data["weighted_average_shares_out"] != 0 else 0
        )
        book_ps = (
            data["total_stockholders_equity"] / data["weighted_average_shares_out"]
            if data["weighted_average_shares_out"] != 0
            else 0
        )
        tangible_ps = (
            data["netTangibleEquity"] / data["weighted_average_shares_out"]
            if data["weighted_average_shares_out"] != 0
            else 0
        )
        fcf_ps = (
            data["free_cash_flow"] / data["weighted_average_shares_out"]
            if data["weighted_average_shares_out"] != 0
            else 0
        )
        eps = (
            data["net_income"] / data["weighted_average_shares_out"] if data["weighted_average_shares_out"] != 0 else 0
        )
        cash_ps = (
            data["cashAndShortTermInvestments"] / data["weighted_average_shares_out"]
            if data["weighted_average_shares_out"] != 0
            else 0
        )
        operating_cf_ps = (
            data["netCashProvidedByOperatingActivities"] / data["weighted_average_shares_out"]
            if data["weighted_average_shares_out"] != 0
            else 0
        )
        capex_ps = (
            data["capital_expenditure"] / data["weighted_average_shares_out"]
            if data["weighted_average_shares_out"] != 0
            else 0
        )
        total_assets_ps = (
            data["total_assets"] / data["weighted_average_shares_out"]
            if data["weighted_average_shares_out"] != 0
            else 0
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
        normalized_income = data["net_income"] - data["totalOtherIncomeExpensesNet"]
        effective_tax_rate = (
            (data["income_tax_expense"] / data["operating_income"]) if data["operating_income"] != 0 else 0
        )
        nopat = data["nopat"]
        net_working_cap = data["total_current_assets"] - data["total_current_liabilities"]
        average_inventory = (data["last_year_inventory"] + data["inventory"]) / 2
        average_payables = (data["last_year_accounts_payable"] + data["account_payables"]) / 2
        divs_per_share = data["dividendsPaid"] / data["commonStock"] if data["commonStock"] != 0 else 0
        dividend_yield = divs_per_share / data["currentPrice"] if data["currentPrice"] != 0 else 0
        earnings_yield = (data["eps"] / data["currentPrice"]) * 100 if data["currentPrice"] != 0 else 0
        fcf_yield = (data["fcf_ps"] / data["currentPrice"]) * 100 if data["currentPrice"] != 0 else 0
        income_quality = (
            (data["netCashProvidedByOperatingActivities"] / data["net_income"]) * 100 if data["net_income"] != 0 else 0
        )
        invested_capital = (
            data["property_plant_equipment_net"] + data["netWorkingCapital"] - data["cash_and_cash_equivalents"]
        )
        market_cap = data["currentPrice"] * data["weighted_average_shares_out"]
        net_current_asset_value = (
            (data["total_current_assets"] - (data["totalLiabilities"])) / data["weighted_average_shares_out"]
            if data["weighted_average_shares_out"] != 0
            else 0
        )
        payout_ratio = abs(data["dividendsPaid"] / data["net_income"]) * 100 if data["net_income"] != 0 else 0
        tangible_assets = data["total_current_assets"] + data["property_plant_equipment_net"]
        retention_ratio = 100 - (
            abs(data["dividendsPaid"] / data["net_income"]) * 100 if data["net_income"] != 0 else 0
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

    def calculate_operation_risk_ratio(self, data: Dict[str, Union[int, float]]) -> Dict[str, Union[int, float]]:
        asset_coverage_ratio = (
            (
                data["total_assets"]
                - data["goodwillAndIntangibleAssets"]
                - data["total_current_liabilities"]
                - data["short_term_debt"]
            )
            / data["interestExpense"]
            if data["interestExpense"] != 0
            else 0
        )
        cash_flow_coverage_ratios = (
            data["netCashProvidedByOperatingActivities"] / data["total_debt"] if data["total_debt"] != 0 else 0
        )
        cash_coverage = (
            data["cashAndShortTermInvestments"] / data["interestExpense"] if data["interestExpense"] != 0 else 0
        )
        debt_service_coverage = data["operating_income"] / data["total_debt"] if data["total_debt"] != 0 else 0
        interest_coverage = data["operating_income"] / data["interestExpense"] if data["interestExpense"] != 0 else 0
        operating_cashflow_ratio = (
            data["netCashProvidedByOperatingActivities"] / data["total_current_liabilities"]
            if data["total_current_liabilities"] != 0
            else 0
        )
        debt_ratio = data["total_debt"] / data["total_assets"] if data["total_assets"] != 0 else 0
        longdebtandcomstock = data["longTermDebt"] + data["commonStock"]
        long_term_debt_to_capitalization = data["longTermDebt"] / longdebtandcomstock if longdebtandcomstock != 0 else 0
        total_debt_to_capitalization = data["total_debt"] / data["debtAndEquity"] if data["debtAndEquity"] != 0 else 0

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

    def calculate_enterprise_value_ratio(self, data: Dict[str, Union[int, float]]) -> Dict[str, Union[int, float]]:
        market_cap = data["currentPrice"] * data["weighted_average_shares_out"]
        enterprise_value = market_cap + data["total_debt"] - data["cashAndShortTermInvestments"]
        ev_fcf = enterprise_value / data["free_cash_flow"] if data["free_cash_flow"] != 0 else 0
        ev_operating_cf = (
            enterprise_value / data["netCashProvidedByOperatingActivities"]
            if data["netCashProvidedByOperatingActivities"] != 0
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
            (data["costAndExpenses"] - data["last_year_cost_expense"]) / data["last_year_cost_expense"]
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

    def calculate_eficiency_ratio(self, data: Dict[str, Union[int, float]]) -> Dict[str, Union[int, float]]:
        days_inventory_outstanding = (
            data["average_inventory"] / (data["cost_of_revenue"] * 360) if data["cost_of_revenue"] != 0 else 0
        )
        days_payables_outstanding = (
            (data["account_payables"] * 360) / data["cost_of_revenue"] if data["cost_of_revenue"] != 0 else 0
        )
        days_sales_outstanding = (
            (data["accountsReceivables"] * 360) / data["account_payables"] if data["account_payables"] != 0 else 0
        )
        operating_cycle = days_inventory_outstanding + days_sales_outstanding
        cash_conversion_cycle = days_inventory_outstanding + days_sales_outstanding - days_sales_outstanding
        asset_turnover = data["revenue"] / data["averageAsssets"] if data["averageAsssets"] != 0 else 0
        inventory_turnover = (
            data["cost_of_revenue"] / data["average_inventory"] if data["average_inventory"] != 0 else 0
        )
        fixed_asset_turnover = data["revenue"] / data["averageFxAs"] if data["averageFxAs"] != 0 else 0
        payables_turnover = data["account_payables"] / data["average_payables"] if data["average_payables"] != 0 else 0
        fcf_to_operating_cf = (
            data["free_cash_flow"] / data["netCashProvidedByOperatingActivities"]
            if data["netCashProvidedByOperatingActivities"] != 0
            else 0
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
            "payables_turnover": payables_turnover,
            "fcf_to_operating_cf": fcf_to_operating_cf,
        }

    def calculate_price_to_ratio(self, data: Dict[str, Union[int, float]]) -> Dict[str, Union[int, float]]:
        price_book = data["currentPrice"] / data["book_ps"] if data["book_ps"] != 0 else 0
        price_cf = data["currentPrice"] / data["cash_ps"] if data["cash_ps"] != 0 else 0
        price_earnings = data["currentPrice"] / data["eps"] if data["eps"] != 0 else 0
        price_earnings_growth = (
            (price_earnings / data["net_income_growth"]).real if data["net_income_growth"] != 0 else 0
        )
        price_sales = data["currentPrice"] / data["sales_ps"] if data["sales_ps"] != 0 else 0
        price_total_assets = data["currentPrice"] / data["total_assets_ps"] if data["total_assets_ps"] != 0 else 0
        price_fcf = data["currentPrice"] / data["fcf_ps"] if data["fcf_ps"] != 0 else 0
        price_operating_cf = data["currentPrice"] / data["operating_cf_ps"] if data["operating_cf_ps"] != 0 else 0
        price_tangible_assets = data["currentPrice"] / data["tangible_ps"] if data["tangible_ps"] != 0 else 0

        return {
            "price_book": price_book,
            "price_cf": price_cf,
            "price_earnings": price_earnings,
            "price_earnings_growth": price_earnings_growth,
            "price_sales": price_sales,
            "price_total_assets": price_total_assets,
            "price_fcf": price_fcf,
            "price_operating_cf": price_operating_cf,
            "price_tangible_assets": price_tangible_assets,
        }
