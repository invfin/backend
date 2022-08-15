from typing import Dict, Union, Any, Type, Callable
import datetime
import pandas as pd


class NormalizeYFinance:
    company = None

    def initial_data(
        self,
        column: Type[pd.Timestamp],
        period: Callable
    ) -> Dict[str, Union[int, datetime.datetime, Callable, Type["Company"]]]:
        return dict(
            date=column.year,
            year=column.to_pydatetime().date(),
            company=self.company,
            period=period(int(column.year))
        )

    def normalize_balance_sheets_yfinance(
        self,
        yfinance_serie: pd.Series,
        column: Type[pd.Timestamp],
        period: Callable
    ) -> Dict[str, Union[float, int, str, Any]]:
        return dict(
            self.initial_data(column, period),
            intangible_assets=yfinance_serie["Intangible Assets"],
            total_liab=yfinance_serie["Total Liab"],
            total_stockholder_equity=yfinance_serie["Total Stockholder Equity"],
            other_current_liab=yfinance_serie["Other Current Liab"],
            total_assets=yfinance_serie["Total Assets"],
            common_stock=yfinance_serie["Common Stock"],
            other_current_assets=yfinance_serie["Other Current Assets"],
            retained_earnings=yfinance_serie["Retained Earnings"],
            other_liab=yfinance_serie["Other Liab"],
            good_will=yfinance_serie["Good Will"],
            gains_losses_not_affecting_retained_earnings=yfinance_serie["Gains Losses Not Affecting Retained Earnings"],
            other_assets=yfinance_serie["Other Assets"],
            cash=yfinance_serie["Cash"],
            total_current_liabilities=yfinance_serie["Total Current Liabilities"],
            deferred_long_term_asset_charges=yfinance_serie["Deferred Long Term Asset Charges"],
            short_long_term_debt=yfinance_serie["Short Long Term Debt"],
            other_stockholder_equity=yfinance_serie["Other Stockholder Equity"],
            property_plant_equipment=yfinance_serie["Property Plant Equipment"],
            total_current_assets=yfinance_serie["Total Current Assets"],
            long_term_investments=yfinance_serie["Long Term Investments"],
            net_tangible_assets=yfinance_serie["Net Tangible Assets"],
            short_term_investments=yfinance_serie["Short Term Investments"],
            net_receivables=yfinance_serie["Net Receivables"],
            long_term_debt=yfinance_serie["Long Term Debt"],
            inventory=yfinance_serie["Inventory"],
            accounts_payable=yfinance_serie["Accounts Payable"]
        )

    def normalize_cashflow_statements_yfinance(
        self,
        yfinance_serie: pd.Series,
        column: Type[pd.Timestamp],
        period: Callable
    ) -> Dict[str, Union[float, int, str, Any]]:
        return dict(
            self.initial_data(column, period),
            investments=yfinance_serie["Investments"],
            change_to_liabilities=yfinance_serie["Change To Liabilities"],
            total_cashflows_from_investing_activities=yfinance_serie["Total Cashflows From Investing Activities"],
            net_borrowings=yfinance_serie["Net Borrowings"],
            total_cash_from_financing_activities=yfinance_serie["Total Cash From Financing Activities"],
            change_to_operating_activities=yfinance_serie["Change To Operating Activities"],
            issuance_of_stock=yfinance_serie["Issuance Of Stock"],
            net_income=yfinance_serie["Net Income"],
            change_in_cash=yfinance_serie["Change In Cash"],
            repurchase_of_stock=yfinance_serie["Repurchase Of Stock"],
            effect_of_exchange_rate=yfinance_serie["Effect Of Exchange Rate"],
            total_cash_from_operating_activities=yfinance_serie["Total Cash From Operating Activities"],
            depreciation=yfinance_serie["Depreciation"],
            other_cashflows_from_investing_activities=yfinance_serie["Other Cashflows From Investing Activities"],
            dividends_paid=yfinance_serie["Dividends Paid"],
            change_to_inventory=yfinance_serie["Change To Inventory"],
            change_to_account_receivables=yfinance_serie["Change To Account Receivables"],
            other_cashflows_from_financing_activities=yfinance_serie["Other Cashflows From Financing Activities"],
            change_to_netincome=yfinance_serie["Change To Netincome"],
            capital_expenditures=yfinance_serie["Capital Expenditures"],
        )

    def normalize_income_statements_yfinance(
        self,
        yfinance_serie: pd.Series,
        column: Type[pd.Timestamp],
        period: Callable
    ) -> Dict[str, Union[float, int, str, Any]]:
        return dict(
            self.initial_data(column, period),
            research_development=yfinance_serie["Research Development"],
            effect_of_accounting_charges=yfinance_serie["Effect Of Accounting Charges"],
            income_before_tax=yfinance_serie["Income Before Tax"],
            minority_interest=yfinance_serie["Minority Interest"],
            net_income=yfinance_serie["Net Income"],
            selling_general_administrative=yfinance_serie["Selling General Administrative"],
            gross_profit=yfinance_serie["Gross Profit"],
            ebit=yfinance_serie["Ebit"],
            operating_income=yfinance_serie["Operating Income"],
            other_operating_expenses=yfinance_serie["Other Operating Expenses"],
            interest_expense=yfinance_serie["Interest Expense"],
            extraordinary_items=yfinance_serie["Extraordinary Items"],
            non_recurring=yfinance_serie["Non Recurring"],
            other_items=yfinance_serie["Other Items"],
            income_tax_expense=yfinance_serie["Income Tax Expense"],
            total_revenue=yfinance_serie["Total Revenue"],
            total_operating_expenses=yfinance_serie["Total Operating Expenses"],
            cost_of_revenue=yfinance_serie["Cost Of Revenue"],
            total_other_income_expense_net=yfinance_serie["Total Other Income Expense Net"],
            discontinued_operations=yfinance_serie["Discontinued Operations"],
            net_income_from_continuing_ops=yfinance_serie["Net Income From Continuing Ops"],
            net_income_applicable_to_common_shares=yfinance_serie["Net Income Applicable To Common Shares"],
        )
