import datetime
from typing import Any, Callable, Dict, Union

import pandas as pd

from src.currencies.models import Currency


class NormalizeYahooQuery:
    company = None

    @staticmethod
    def initial_data(
        date: pd.Timestamp,
        period_type,
        period: Callable,
        currency,
        company,
    ) -> Dict[str, Union[int, datetime.datetime, type]]:
        return dict(
            date=date.date().year,
            year=date.to_pydatetime().date(),
            company=company,
            period=period(date.year),
            reported_currency=Currency.objects.financial_currency(currency),
            as_of_date=date,
            period_type=period_type,
            currency_code=currency,
        )

    @classmethod
    def normalize_balance_sheets_yahooquery(
        cls,
        yahooquery_serie: pd.Series,
        period: Callable,
        company,
    ) -> Dict[str, Union[float, int, str, Any]]:
        return dict(
            **cls.initial_data(
                yahooquery_serie.get("asOfDate"),
                yahooquery_serie.get("periodType"),
                period,
                yahooquery_serie.get("currencyCode"),
                company,
            ),
            accounts_payable=yahooquery_serie.get("AccountsPayable"),
            accounts_receivable=yahooquery_serie.get("AccountsReceivable"),
            accumulated_depreciation=yahooquery_serie.get("AccumulatedDepreciation"),
            available_for_sale_securities=yahooquery_serie.get("AvailableForSaleSecurities"),
            capital_stock=yahooquery_serie.get("CapitalStock"),
            cash_and_cash_equivalents=yahooquery_serie.get("CashAndCashEquivalents"),
            cash_cash_equivalents_and_short_term_investments=yahooquery_serie.get(
                "CashCashEquivalentsAndShortTermInvestments"
            ),
            cash_equivalents=yahooquery_serie.get("CashEquivalents"),
            cash_financial=yahooquery_serie.get("CashFinancial"),
            commercial_paper=yahooquery_serie.get("CommercialPaper"),
            common_stock=yahooquery_serie.get("CommonStock"),
            common_stock_equity=yahooquery_serie.get("CommonStockEquity"),
            current_assets=yahooquery_serie.get("CurrentAssets"),
            current_debt=yahooquery_serie.get("CurrentDebt"),
            current_debt_and_capital_lease_obligation=yahooquery_serie.get(
                "CurrentDebtAndCapitalLeaseObligation"
            ),
            current_deferred_liabilities=yahooquery_serie.get("CurrentDeferredLiabilities"),
            current_deferred_revenue=yahooquery_serie.get("CurrentDeferredRevenue"),
            current_liabilities=yahooquery_serie.get("CurrentLiabilities"),
            gains_losses_not_affecting_retained_earnings=yahooquery_serie.get(
                "GainsLossesNotAffectingRetainedEarnings"
            ),
            gross_ppe=yahooquery_serie.get("GrossPPE"),
            inventory=yahooquery_serie.get("Inventory"),
            invested_capital=yahooquery_serie.get("InvestedCapital"),
            # TODO: change investmentin_financial_assets into investment_in_financial_assets
            investmentin_financial_assets=yahooquery_serie.get("InvestmentinFinancialAssets"),
            investments_and_advances=yahooquery_serie.get("InvestmentsAndAdvances"),
            land_and_improvements=yahooquery_serie.get("LandAndImprovements"),
            leases=yahooquery_serie.get("Leases"),
            long_term_debt=yahooquery_serie.get("LongTermDebt"),
            long_term_debt_and_capital_lease_obligation=yahooquery_serie.get(
                "LongTermDebtAndCapitalLeaseObligation"
            ),
            machinery_furniture_equipment=yahooquery_serie.get("MachineryFurnitureEquipment"),
            net_debt=yahooquery_serie.get("NetDebt"),
            net_ppe=yahooquery_serie.get("NetPPE"),
            net_tangible_assets=yahooquery_serie.get("NetTangibleAssets"),
            non_current_deferred_liabilities=yahooquery_serie.get(
                "NonCurrentDeferredLiabilities"
            ),
            non_current_deferred_revenue=yahooquery_serie.get("NonCurrentDeferredRevenue"),
            non_current_deferred_taxes_liabilities=yahooquery_serie.get(
                "NonCurrentDeferredTaxesLiabilities"
            ),
            ordinary_shares_number=yahooquery_serie.get("OrdinarySharesNumber"),
            other_current_assets=yahooquery_serie.get("OtherCurrentAssets"),
            other_current_borrowings=yahooquery_serie.get("OtherCurrentBorrowings"),
            other_current_liabilities=yahooquery_serie.get("OtherCurrentLiabilities"),
            other_non_current_assets=yahooquery_serie.get("OtherNonCurrentAssets"),
            other_non_current_liabilities=yahooquery_serie.get("OtherNonCurrentLiabilities"),
            other_receivables=yahooquery_serie.get("OtherReceivables"),
            other_short_term_investments=yahooquery_serie.get("OtherShortTermInvestments"),
            payables=yahooquery_serie.get("Payables"),
            payables_and_accrued_expenses=yahooquery_serie.get("PayablesAndAccruedExpenses"),
            properties=yahooquery_serie.get("Properties"),
            receivables=yahooquery_serie.get("Receivables"),
            retained_earnings=yahooquery_serie.get("RetainedEarnings"),
            share_issued=yahooquery_serie.get("ShareIssued"),
            stockholders_equity=yahooquery_serie.get("StockholdersEquity"),
            tangible_book_value=yahooquery_serie.get("TangibleBookValue"),
            total_assets=yahooquery_serie.get("TotalAssets"),
            total_capitalization=yahooquery_serie.get("TotalCapitalization"),
            total_debt=yahooquery_serie.get("TotalDebt"),
            total_equity_gross_minority_interest=yahooquery_serie.get(
                "TotalEquityGrossMinorityInterest"
            ),
            total_liabilities_net_minority_interest=yahooquery_serie.get(
                "TotalLiabilitiesNetMinorityInterest"
            ),
            total_non_current_assets=yahooquery_serie.get("TotalNonCurrentAssets"),
            total_non_current_liabilities_net_minority_interest=yahooquery_serie.get(
                "TotalNonCurrentLiabilitiesNetMinorityInterest"
            ),
            tradeand_other_payables_non_current=yahooquery_serie.get(
                "TradeandOtherPayablesNonCurrent"
            ),
            working_capital=yahooquery_serie.get("WorkingCapital"),
        )

    @classmethod
    def normalize_cashflow_statements_yahooquery(
        cls,
        yahooquery_serie: pd.Series,
        period: Callable,
        company,
    ) -> Dict[str, Union[float, int, str, Any]]:
        return dict(
            **cls.initial_data(
                yahooquery_serie.get("asOfDate"),
                yahooquery_serie.get("periodType"),
                period,
                yahooquery_serie.get("currencyCode"),
                company,
            ),
            beginning_cash_position=yahooquery_serie.get("BeginningCashPosition"),
            capital_expenditure=yahooquery_serie.get("CapitalExpenditure"),
            cash_dividends_paid=yahooquery_serie.get("CashDividendsPaid"),
            cash_flow_from_continuing_financing_activities=yahooquery_serie.get(
                "CashFlowFromContinuingFinancingActivities"
            ),
            cash_flow_from_continuing_investing_activities=yahooquery_serie.get(
                "CashFlowFromContinuingInvestingActivities"
            ),
            cash_flow_from_continuing_operating_activities=yahooquery_serie.get(
                "CashFlowFromContinuingOperatingActivities"
            ),
            change_in_account_payable=yahooquery_serie.get("ChangeInAccountPayable"),
            change_in_cash_supplemental_as_reported=yahooquery_serie.get(
                "ChangeInCashSupplementalAsReported"
            ),
            change_in_inventory=yahooquery_serie.get("ChangeInInventory"),
            change_in_other_current_assets=yahooquery_serie.get("ChangeInOtherCurrentAssets"),
            change_in_other_current_liabilities=yahooquery_serie.get(
                "ChangeInOtherCurrentLiabilities"
            ),
            change_in_other_working_capital=yahooquery_serie.get(
                "ChangeInOtherWorkingCapital"
            ),
            change_in_payable=yahooquery_serie.get("ChangeInPayable"),
            change_in_payables_and_accrued_expense=yahooquery_serie.get(
                "ChangeInPayablesAndAccruedExpense"
            ),
            change_in_receivables=yahooquery_serie.get("ChangeInReceivables"),
            change_in_working_capital=yahooquery_serie.get("ChangeInWorkingCapital"),
            changes_in_account_receivables=yahooquery_serie.get("ChangesInAccountReceivables"),
            changes_in_cash=yahooquery_serie.get("ChangesInCash"),
            common_stock_dividend_paid=yahooquery_serie.get("CommonStockDividendPaid"),
            common_stock_issuance=yahooquery_serie.get("CommonStockIssuance"),
            common_stock_payments=yahooquery_serie.get("CommonStockPayments"),
            deferred_income_tax=yahooquery_serie.get("DeferredIncomeTax"),
            deferred_tax=yahooquery_serie.get("DeferredTax"),
            depreciation_amortization_depletion=yahooquery_serie.get(
                "DepreciationAmortizationDepletion"
            ),
            depreciation_and_amortization=yahooquery_serie.get("DepreciationAndAmortization"),
            end_cash_position=yahooquery_serie.get("EndCashPosition"),
            financing_cash_flow=yahooquery_serie.get("FinancingCashFlow"),
            free_cash_flow=yahooquery_serie.get("FreeCashFlow"),
            income_tax_paid_supplemental_data=yahooquery_serie.get(
                "IncomeTaxPaidSupplementalData"
            ),
            interest_paid_supplemental_data=yahooquery_serie.get(
                "InterestPaidSupplementalData"
            ),
            investing_cash_flow=yahooquery_serie.get("InvestingCashFlow"),
            issuance_of_capital_stock=yahooquery_serie.get("IssuanceOfCapitalStock"),
            issuance_of_debt=yahooquery_serie.get("IssuanceOfDebt"),
            long_term_debt_issuance=yahooquery_serie.get("LongTermDebtIssuance"),
            long_term_debt_payments=yahooquery_serie.get("LongTermDebtPayments"),
            net_business_purchase_and_sale=yahooquery_serie.get("NetBusinessPurchaseAndSale"),
            net_common_stock_issuance=yahooquery_serie.get("NetCommonStockIssuance"),
            net_income=yahooquery_serie.get("NetIncome"),
            net_income_from_continuing_operations=yahooquery_serie.get(
                "NetIncomeFromContinuingOperations"
            ),
            net_investment_purchase_and_sale=yahooquery_serie.get(
                "NetInvestmentPurchaseAndSale"
            ),
            net_issuance_payments_of_debt=yahooquery_serie.get("NetIssuancePaymentsOfDebt"),
            net_long_term_debt_issuance=yahooquery_serie.get("NetLongTermDebtIssuance"),
            net_other_financing_charges=yahooquery_serie.get("NetOtherFinancingCharges"),
            net_other_investing_changes=yahooquery_serie.get("NetOtherInvestingChanges"),
            net_ppe_purchase_and_sale=yahooquery_serie.get("NetPPEPurchaseAndSale"),
            net_short_term_debt_issuance=yahooquery_serie.get("NetShortTermDebtIssuance"),
            operating_cash_flow=yahooquery_serie.get("OperatingCashFlow"),
            other_non_cash_items=yahooquery_serie.get("OtherNonCashItems"),
            purchase_of_business=yahooquery_serie.get("PurchaseOfBusiness"),
            purchase_of_investment=yahooquery_serie.get("PurchaseOfInvestment"),
            purchase_of_ppe=yahooquery_serie.get("PurchaseOfPPE"),
            repayment_of_debt=yahooquery_serie.get("RepaymentOfDebt"),
            repurchase_of_capital_stock=yahooquery_serie.get("RepurchaseOfCapitalStock"),
            sale_of_investment=yahooquery_serie.get("SaleOfInvestment"),
            short_term_debt_payments=yahooquery_serie.get("ShortTermDebtPayments"),
            stock_based_compensation=yahooquery_serie.get("StockBasedCompensation"),
        )

    @classmethod
    def normalize_income_statements_yahooquery(
        cls,
        yahooquery_serie: pd.Series,
        period: Callable,
        company,
    ) -> Dict[str, Union[float, int, str, Any]]:
        return dict(
            **cls.initial_data(
                yahooquery_serie.get("asOfDate"),
                yahooquery_serie.get("periodType"),
                period,
                yahooquery_serie.get("currencyCode"),
                company,
            ),
            basic_average_shares=yahooquery_serie.get("BasicAverageShares"),
            basic_eps=yahooquery_serie.get("BasicEPS"),
            cost_of_revenue=yahooquery_serie.get("CostOfRevenue"),
            diluted_average_shares=yahooquery_serie.get("DilutedAverageShares"),
            diluted_eps=yahooquery_serie.get("DilutedEPS"),
            diluted_ni_availto_com_stockholders=yahooquery_serie.get(
                "DilutedNIAvailtoComStockholders"
            ),
            ebit=yahooquery_serie.get("EBIT"),
            ebitda=yahooquery_serie.get("EBITDA"),
            gross_profit=yahooquery_serie.get("GrossProfit"),
            interest_expense=yahooquery_serie.get("InterestExpense"),
            interest_expense_non_operating=yahooquery_serie.get("InterestExpenseNonOperating"),
            interest_income=yahooquery_serie.get("InterestIncome"),
            interest_income_non_operating=yahooquery_serie.get("InterestIncomeNonOperating"),
            net_income=yahooquery_serie.get("NetIncome"),
            net_income_common_stockholders=yahooquery_serie.get("NetIncomeCommonStockholders"),
            net_income_continuous_operations=yahooquery_serie.get(
                "NetIncomeContinuousOperations"
            ),
            net_income_from_continuing_and_discontinued_operation=yahooquery_serie.get(
                "NetIncomeFromContinuingAndDiscontinuedOperation"
            ),
            net_income_from_continuing_operation_net_minority_interest=yahooquery_serie.get(
                "NetIncomeFromContinuingOperationNetMinorityInterest"
            ),
            net_income_including_noncontrolling_interests=yahooquery_serie.get(
                "NetIncomeIncludingNoncontrollingInterests"
            ),
            net_interest_income=yahooquery_serie.get("NetInterestIncome"),
            net_non_operating_interest_income_expense=yahooquery_serie.get(
                "NetNonOperatingInterestIncomeExpense"
            ),
            normalized_ebitda=yahooquery_serie.get("NormalizedEBITDA"),
            normalized_income=yahooquery_serie.get("NormalizedIncome"),
            operating_expense=yahooquery_serie.get("OperatingExpense"),
            operating_income=yahooquery_serie.get("OperatingIncome"),
            operating_revenue=yahooquery_serie.get("OperatingRevenue"),
            other_income_expense=yahooquery_serie.get("OtherIncomeExpense"),
            other_non_operating_income_expenses=yahooquery_serie.get(
                "OtherNonOperatingIncomeExpenses"
            ),
            pretax_income=yahooquery_serie.get("PretaxIncome"),
            reconciled_cost_of_revenue=yahooquery_serie.get("ReconciledCostOfRevenue"),
            reconciled_depreciation=yahooquery_serie.get("ReconciledDepreciation"),
            research_and_development=yahooquery_serie.get("ResearchAndDevelopment"),
            selling_general_and_administration=yahooquery_serie.get(
                "SellingGeneralAndAdministration"
            ),
            tax_effect_of_unusual_items=yahooquery_serie.get("TaxEffectOfUnusualItems"),
            tax_provision=yahooquery_serie.get("TaxProvision"),
            tax_rate_for_calcs=yahooquery_serie.get("TaxRateForCalcs"),
            total_expenses=yahooquery_serie.get("TotalExpenses"),
            total_operating_income_as_reported=yahooquery_serie.get(
                "TotalOperatingIncomeAsReported"
            ),
            total_revenue=yahooquery_serie.get("TotalRevenue"),
        )

    @staticmethod
    def normalize_institutional_yahooquery(df_institution_ownership):
        df = df_institution_ownership.reset_index()
        df = df.drop(columns=["symbol", "row", "maxAge"])
        return df

    @staticmethod
    def normalize_key_stats_yahooquery(key_stats, company):
        last_fiscal_year_end = key_stats.get("lastFiscalYearEnd")
        next_fiscal_year_end = key_stats.get("nextFiscalYearEnd")
        most_recent_quarter = key_stats.get("mostRecentQuarter")
        last_split_date = key_stats.get("lastSplitDate")
        if last_split_date:
            last_split_date = (
                datetime.datetime.strptime(last_split_date, "%Y-%m-%d %H:%M:%S")
                .date()
                .strftime("%Y-%m-%d")
            )
        if last_fiscal_year_end:
            last_fiscal_year_end = (
                datetime.datetime.strptime(last_fiscal_year_end, "%Y-%m-%d %H:%M:%S")
                .date()
                .strftime("%Y-%m-%d")
            )
        if next_fiscal_year_end:
            next_fiscal_year_end = (
                datetime.datetime.strptime(next_fiscal_year_end, "%Y-%m-%d %H:%M:%S")
                .date()
                .strftime("%Y-%m-%d")
            )
        if most_recent_quarter:
            most_recent_quarter = (
                datetime.datetime.strptime(most_recent_quarter, "%Y-%m-%d %H:%M:%S")
                .date()
                .strftime("%Y-%m-%d")
            )
        return dict(
            financials=key_stats,
            date=datetime.datetime.now().year,
            year=datetime.datetime.now().date(),
            company=company,
            max_age=key_stats.get("maxAge"),
            price_hint=key_stats.get("priceHint"),
            enterprise_value=key_stats.get("enterpriseValue"),
            forward_pe=key_stats.get("forwardPE"),
            profit_margins=key_stats.get("profitMargins"),
            float_shares=key_stats.get("floatShares"),
            shares_outstanding=key_stats.get("sharesOutstanding"),
            shares_short=key_stats.get("sharesShort"),
            shares_short_prior_month=key_stats.get("sharesShortPriorMonth"),
            shares_short_previous_month_date=key_stats.get("sharesShortPreviousMonthDate"),
            date_short_interest=key_stats.get("dateShortInterest"),
            shares_percent_shares_out=key_stats.get("sharesPercentSharesOut"),
            held_percent_insiders=key_stats.get("heldPercentInsiders"),
            held_percent_institutions=key_stats.get("heldPercentInstitutions"),
            short_ratio=key_stats.get("shortRatio"),
            short_percent_of_float=key_stats.get("shortPercentOfFloat"),
            beta=key_stats.get("beta"),
            category=key_stats.get("category"),
            book_value=key_stats.get("bookValue"),
            price_to_book=key_stats.get("priceToBook"),
            fund_family=key_stats.get("fundFamily"),
            legal_type=key_stats.get("legalType"),
            last_fiscal_year_end=last_fiscal_year_end,
            next_fiscal_year_end=next_fiscal_year_end,
            most_recent_quarter=most_recent_quarter,
            earnings_quarterly_growth=key_stats.get("earningsQuarterlyGrowth"),
            net_income_to_common=key_stats.get("netIncomeToCommon"),
            trailing_eps=key_stats.get("trailingEps"),
            forward_eps=key_stats.get("forwardEps"),
            peg_ratio=key_stats.get("pegRatio"),
            last_split_factor=key_stats.get("lastSplitFactor"),
            last_split_date=last_split_date,
            enterprise_to_revenue=key_stats.get("enterpriseToRevenue"),
            enterprise_to_ebitda=key_stats.get("enterpriseToEbitda"),
            week_change_52=key_stats.get("52WeekChange"),
            sand_p52_week_change=key_stats.get("SandP52WeekChange"),
        )
