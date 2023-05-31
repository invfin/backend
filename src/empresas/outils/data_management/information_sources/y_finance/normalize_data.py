import datetime
from typing import Any, Callable, Dict, Type, Union

import pandas as pd


class NormalizeYFinance:
    company = None

    def initial_data(
        self,
        column: pd.Timestamp,
        period: Callable,
    ) -> Dict[str, Union[int, datetime.datetime, Callable, Type]]:
        return dict(
            date=column.year, year=column.to_pydatetime().date(), company=self.company, period=period(int(column.year))
        )

    def normalize_balance_sheets_yfinance(
        self, yfinance_serie: pd.Series, column: pd.Timestamp, period: Callable
    ) -> Dict[str, Union[float, int, str, Any]]:
        return dict(
            **self.initial_data(column, period),
            intangible_assets=yfinance_serie.get("Intangible Assets"),
            total_liab=yfinance_serie.get("Total Liab"),
            total_stockholder_equity=yfinance_serie.get("Total Stockholder Equity"),
            other_current_liab=yfinance_serie.get("Other Current Liab"),
            total_assets=yfinance_serie.get("Total Assets"),
            common_stock=yfinance_serie.get("Common Stock"),
            other_current_assets=yfinance_serie.get("Other Current Assets"),
            retained_earnings=yfinance_serie.get("Retained Earnings"),
            other_liab=yfinance_serie.get("Other Liab"),
            good_will=yfinance_serie.get("Good Will"),
            gains_losses_not_affecting_retained_earnings=yfinance_serie.get(
                "Gains Losses Not Affecting Retained Earnings"
            ),
            other_assets=yfinance_serie.get("Other Assets"),
            cash=yfinance_serie.get("Cash"),
            total_current_liabilities=yfinance_serie.get("Total Current Liabilities"),
            deferred_long_term_asset_charges=yfinance_serie.get("Deferred Long Term Asset Charges"),
            short_long_term_debt=yfinance_serie.get("Short Long Term Debt"),
            other_stockholder_equity=yfinance_serie.get("Other Stockholder Equity"),
            property_plant_equipment=yfinance_serie.get("Property Plant Equipment"),
            total_current_assets=yfinance_serie.get("Total Current Assets"),
            long_term_investments=yfinance_serie.get("Long Term Investments"),
            net_tangible_assets=yfinance_serie.get("Net Tangible Assets"),
            short_term_investments=yfinance_serie.get("Short Term Investments"),
            net_receivables=yfinance_serie.get("Net Receivables"),
            long_term_debt=yfinance_serie.get("Long Term Debt"),
            inventory=yfinance_serie.get("Inventory"),
            accounts_payable=yfinance_serie.get("Accounts Payable"),
        )

    def normalize_cashflow_statements_yfinance(
        self, yfinance_serie: pd.Series, column: pd.Timestamp, period: Callable
    ) -> Dict[str, Union[float, int, str, Any]]:
        return dict(
            **self.initial_data(column, period),
            investments=yfinance_serie.get("Investments"),
            change_to_liabilities=yfinance_serie.get("Change To Liabilities"),
            total_cashflows_from_investing_activities=yfinance_serie.get("Total Cashflows From Investing Activities"),
            net_borrowings=yfinance_serie.get("Net Borrowings"),
            total_cash_from_financing_activities=yfinance_serie.get("Total Cash From Financing Activities"),
            change_to_operating_activities=yfinance_serie.get("Change To Operating Activities"),
            issuance_of_stock=yfinance_serie.get("Issuance Of Stock"),
            net_income=yfinance_serie.get("Net Income"),
            change_in_cash=yfinance_serie.get("Change In Cash"),
            repurchase_of_stock=yfinance_serie.get("Repurchase Of Stock"),
            effect_of_exchange_rate=yfinance_serie.get("Effect Of Exchange Rate"),
            total_cash_from_operating_activities=yfinance_serie.get("Total Cash From Operating Activities"),
            depreciation=yfinance_serie.get("Depreciation"),
            other_cashflows_from_investing_activities=yfinance_serie.get("Other Cashflows From Investing Activities"),
            dividends_paid=yfinance_serie.get("Dividends Paid"),
            change_to_inventory=yfinance_serie.get("Change To Inventory"),
            change_to_account_receivables=yfinance_serie.get("Change To Account Receivables"),
            other_cashflows_from_financing_activities=yfinance_serie.get("Other Cashflows From Financing Activities"),
            change_to_netincome=yfinance_serie.get("Change To Netincome"),
            capital_expenditures=yfinance_serie.get("Capital Expenditures"),
        )

    def normalize_income_statements_yfinance(
        self, yfinance_serie: pd.Series, column: pd.Timestamp, period: Callable
    ) -> Dict[str, Union[float, int, str, Any]]:
        return dict(
            **self.initial_data(column, period),
            research_development=yfinance_serie.get("Research Development"),
            effect_of_accounting_charges=yfinance_serie.get("Effect Of Accounting Charges"),
            income_before_tax=yfinance_serie.get("Income Before Tax"),
            minority_interest=yfinance_serie.get("Minority Interest"),
            net_income=yfinance_serie.get("Net Income"),
            selling_general_administrative=yfinance_serie.get("Selling General Administrative"),
            gross_profit=yfinance_serie.get("Gross Profit"),
            ebit=yfinance_serie.get("Ebit"),
            operating_income=yfinance_serie.get("Operating Income"),
            other_operating_expenses=yfinance_serie.get("Other Operating Expenses"),
            interest_expense=yfinance_serie.get("Interest Expense"),
            extraordinary_items=yfinance_serie.get("Extraordinary Items"),
            non_recurring=yfinance_serie.get("Non Recurring"),
            other_items=yfinance_serie.get("Other Items"),
            income_tax_expense=yfinance_serie.get("Income Tax Expense"),
            total_revenue=yfinance_serie.get("Total Revenue"),
            total_operating_expenses=yfinance_serie.get("Total Operating Expenses"),
            cost_of_revenue=yfinance_serie.get("Cost Of Revenue"),
            total_other_income_expense_net=yfinance_serie.get("Total Other Income Expense Net"),
            discontinued_operations=yfinance_serie.get("Discontinued Operations"),
            net_income_from_continuing_ops=yfinance_serie.get("Net Income From Continuing Ops"),
            net_income_applicable_to_common_shares=yfinance_serie.get("Net Income Applicable To Common Shares"),
        )
