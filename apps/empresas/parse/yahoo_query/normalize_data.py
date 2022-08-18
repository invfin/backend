from typing import Dict, Union, Any, Type, Callable
import datetime
import pandas as pd

from apps.general.models import Currency


class NormalizeYahooQuery:
    def __init__(self, company) -> None:
        self.company = company

    def initial_data(
        self,
        date: Type[pd.Timestamp],
        period: Callable,
        currency
    )-> Dict[str, Union[int, datetime.datetime, Type["Company"]]]:
        return dict(
            date=date.year,
            year=date.to_pydatetime().date(),
            company=self.company,
            period=period(date.year),
            reported_currency=Currency.objects.financial_currency(currency)
        )

    def normalize_balance_sheets_yahooquery(
        self,
        yahooquery_serie: pd.Series,
        period: Callable
    )-> Dict[str, Union[float, int, str, Any]]:
        return dict(
            self.initial_data(yahooquery_serie["asOfDate"], period, yahooquery_serie["currencyCode"]),
            as_of_date=yahooquery_serie["asOfDate"],
            period_type=yahooquery_serie["periodType"],
            currency_code=yahooquery_serie["currencyCode"],
            accounts_payable=yahooquery_serie["AccountsPayable"],
            accounts_receivable=yahooquery_serie["AccountsReceivable"],
            accumulated_depreciation=yahooquery_serie["AccumulatedDepreciation"],
            available_for_sale_securities=yahooquery_serie["AvailableForSaleSecurities"],
            capital_stock=yahooquery_serie["CapitalStock"],
            cash_and_cash_equivalents=yahooquery_serie["CashAndCashEquivalents"],
            cash_cash_equivalents_and_short_term_investments=yahooquery_serie["CashCashEquivalentsAndShortTermInvestments"],
            cash_equivalents=yahooquery_serie["CashEquivalents"],
            cash_financial=yahooquery_serie["CashFinancial"],
            commercial_paper=yahooquery_serie["CommercialPaper"],
            common_stock=yahooquery_serie["CommonStock"],
            common_stock_equity=yahooquery_serie["CommonStockEquity"],
            current_assets=yahooquery_serie["CurrentAssets"],
            current_debt=yahooquery_serie["CurrentDebt"],
            current_debt_and_capital_lease_obligation=yahooquery_serie["CurrentDebtAndCapitalLeaseObligation"],
            current_deferred_liabilities=yahooquery_serie["CurrentDeferredLiabilities"],
            current_deferred_revenue=yahooquery_serie["CurrentDeferredRevenue"],
            current_liabilities=yahooquery_serie["CurrentLiabilities"],
            gains_losses_not_affecting_retained_earnings=yahooquery_serie["GainsLossesNotAffectingRetainedEarnings"],
            gross_ppe=yahooquery_serie["GrossPPE"],
            inventory=yahooquery_serie["Inventory"],
            invested_capital=yahooquery_serie["InvestedCapital"],
            investmentin_financial_assets=yahooquery_serie["InvestmentinFinancialAssets"],
            investments_and_advances=yahooquery_serie["InvestmentsAndAdvances"],
            land_and_improvements=yahooquery_serie["LandAndImprovements"],
            leases=yahooquery_serie["Leases"],
            long_term_debt=yahooquery_serie["LongTermDebt"],
            long_term_debt_and_capital_lease_obligation=yahooquery_serie["LongTermDebtAndCapitalLeaseObligation"],
            machinery_furniture_equipment=yahooquery_serie["MachineryFurnitureEquipment"],
            net_debt=yahooquery_serie["NetDebt"],
            net_ppe=yahooquery_serie["NetPPE"],
            net_tangible_assets=yahooquery_serie["NetTangibleAssets"],
            non_current_deferred_liabilities=yahooquery_serie["NonCurrentDeferredLiabilities"],
            non_current_deferred_revenue=yahooquery_serie["NonCurrentDeferredRevenue"],
            non_current_deferred_taxes_liabilities=yahooquery_serie["NonCurrentDeferredTaxesLiabilities"],
            ordinary_shares_number=yahooquery_serie["OrdinarySharesNumber"],
            other_current_assets=yahooquery_serie["OtherCurrentAssets"],
            other_current_borrowings=yahooquery_serie["OtherCurrentBorrowings"],
            other_current_liabilities=yahooquery_serie["OtherCurrentLiabilities"],
            other_non_current_assets=yahooquery_serie["OtherNonCurrentAssets"],
            other_non_current_liabilities=yahooquery_serie["OtherNonCurrentLiabilities"],
            other_receivables=yahooquery_serie["OtherReceivables"],
            other_short_term_investments=yahooquery_serie["OtherShortTermInvestments"],
            payables=yahooquery_serie["Payables"],
            payables_and_accrued_expenses=yahooquery_serie["PayablesAndAccruedExpenses"],
            properties=yahooquery_serie["Properties"],
            receivables=yahooquery_serie["Receivables"],
            retained_earnings=yahooquery_serie["RetainedEarnings"],
            share_issued=yahooquery_serie["ShareIssued"],
            stockholders_equity=yahooquery_serie["StockholdersEquity"],
            tangible_book_value=yahooquery_serie["TangibleBookValue"],
            total_assets=yahooquery_serie["TotalAssets"],
            total_capitalization=yahooquery_serie["TotalCapitalization"],
            total_debt=yahooquery_serie["TotalDebt"],
            total_equity_gross_minority_interest=yahooquery_serie["TotalEquityGrossMinorityInterest"],
            total_liabilities_net_minority_interest=yahooquery_serie["TotalLiabilitiesNetMinorityInterest"],
            total_non_current_assets=yahooquery_serie["TotalNonCurrentAssets"],
            total_non_current_liabilities_net_minority_interest=yahooquery_serie["TotalNonCurrentLiabilitiesNetMinorityInterest"],
            tradeand_other_payables_non_current=yahooquery_serie["TradeandOtherPayablesNonCurrent"],
            working_capital=yahooquery_serie["WorkingCapital"]
        )

    def normalize_cashflow_statements_yahooquery(
        self,
        yahooquery_serie: pd.Series,
        period: Callable
    )-> Dict[str, Union[float, int, str, Any]]:
        return dict(
            self.initial_data(yahooquery_serie["asOfDate"], period, yahooquery_serie["currencyCode"]),
            as_of_date=yahooquery_serie["asOfDate"],
            period_type=yahooquery_serie["periodType"],
            currency_code=yahooquery_serie["currencyCode"],
            beginning_cash_position=yahooquery_serie["BeginningCashPosition"],
            capital_expenditure=yahooquery_serie["CapitalExpenditure"],
            cash_dividends_paid=yahooquery_serie["CashDividendsPaid"],
            cash_flow_from_continuing_financing_activities=yahooquery_serie["CashFlowFromContinuingFinancingActivities"],
            cash_flow_from_continuing_investing_activities=yahooquery_serie["CashFlowFromContinuingInvestingActivities"],
            cash_flow_from_continuing_operating_activities=yahooquery_serie["CashFlowFromContinuingOperatingActivities"],
            change_in_account_payable=yahooquery_serie["ChangeInAccountPayable"],
            change_in_cash_supplemental_as_reported=yahooquery_serie["ChangeInCashSupplementalAsReported"],
            change_in_inventory=yahooquery_serie["ChangeInInventory"],
            change_in_other_current_assets=yahooquery_serie["ChangeInOtherCurrentAssets"],
            change_in_other_current_liabilities=yahooquery_serie["ChangeInOtherCurrentLiabilities"],
            change_in_other_working_capital=yahooquery_serie["ChangeInOtherWorkingCapital"],
            change_in_payable=yahooquery_serie["ChangeInPayable"],
            change_in_payables_and_accrued_expense=yahooquery_serie["ChangeInPayablesAndAccruedExpense"],
            change_in_receivables=yahooquery_serie["ChangeInReceivables"],
            change_in_working_capital=yahooquery_serie["ChangeInWorkingCapital"],
            changes_in_account_receivables=yahooquery_serie["ChangesInAccountReceivables"],
            changes_in_cash=yahooquery_serie["ChangesInCash"],
            common_stock_dividend_paid=yahooquery_serie["CommonStockDividendPaid"],
            common_stock_issuance=yahooquery_serie["CommonStockIssuance"],
            common_stock_payments=yahooquery_serie["CommonStockPayments"],
            deferred_income_tax=yahooquery_serie["DeferredIncomeTax"],
            deferred_tax=yahooquery_serie["DeferredTax"],
            depreciation_amortization_depletion=yahooquery_serie["DepreciationAmortizationDepletion"],
            depreciation_and_amortization=yahooquery_serie["DepreciationAndAmortization"],
            end_cash_position=yahooquery_serie["EndCashPosition"],
            financing_cash_flow=yahooquery_serie["FinancingCashFlow"],
            free_cash_flow=yahooquery_serie["FreeCashFlow"],
            income_tax_paid_supplemental_data=yahooquery_serie["IncomeTaxPaidSupplementalData"],
            interest_paid_supplemental_data=yahooquery_serie["InterestPaidSupplementalData"],
            investing_cash_flow=yahooquery_serie["InvestingCashFlow"],
            issuance_of_capital_stock=yahooquery_serie["IssuanceOfCapitalStock"],
            issuance_of_debt=yahooquery_serie["IssuanceOfDebt"],
            long_term_debt_issuance=yahooquery_serie["LongTermDebtIssuance"],
            long_term_debt_payments=yahooquery_serie["LongTermDebtPayments"],
            net_business_purchase_and_sale=yahooquery_serie["NetBusinessPurchaseAndSale"],
            net_common_stock_issuance=yahooquery_serie["NetCommonStockIssuance"],
            net_income=yahooquery_serie["NetIncome"],
            net_income_from_continuing_operations=yahooquery_serie["NetIncomeFromContinuingOperations"],
            net_investment_purchase_and_sale=yahooquery_serie["NetInvestmentPurchaseAndSale"],
            net_issuance_payments_of_debt=yahooquery_serie["NetIssuancePaymentsOfDebt"],
            net_long_term_debt_issuance=yahooquery_serie["NetLongTermDebtIssuance"],
            net_other_financing_charges=yahooquery_serie["NetOtherFinancingCharges"],
            net_other_investing_changes=yahooquery_serie["NetOtherInvestingChanges"],
            net_ppe_purchase_and_sale=yahooquery_serie["NetPPEPurchaseAndSale"],
            net_short_term_debt_issuance=yahooquery_serie["NetShortTermDebtIssuance"],
            operating_cash_flow=yahooquery_serie["OperatingCashFlow"],
            other_non_cash_items=yahooquery_serie["OtherNonCashItems"],
            purchase_of_business=yahooquery_serie["PurchaseOfBusiness"],
            purchase_of_investment=yahooquery_serie["PurchaseOfInvestment"],
            purchase_of_ppe=yahooquery_serie["PurchaseOfPPE"],
            repayment_of_debt=yahooquery_serie["RepaymentOfDebt"],
            repurchase_of_capital_stock=yahooquery_serie["RepurchaseOfCapitalStock"],
            sale_of_investment=yahooquery_serie["SaleOfInvestment"],
            short_term_debt_payments=yahooquery_serie["ShortTermDebtPayments"],
            stock_based_compensation=yahooquery_serie["StockBasedCompensation"])


    def normalize_income_statements_yahooquery(
        self,
        yahooquery_serie: pd.Series,
        period: Callable
    )-> Dict[str, Union[float, int, str, Any]]:
        return dict(
            self.initial_data(yahooquery_serie["asOfDate"], period, yahooquery_serie["currencyCode"]),
            as_of_date=yahooquery_serie["asOfDate"],
            period_type=yahooquery_serie["periodType"],
            currency_code=yahooquery_serie["currencyCode"],
            basic_average_shares=yahooquery_serie["BasicAverageShares"],
            basic_eps=yahooquery_serie["BasicEPS"],
            cost_of_revenue=yahooquery_serie["CostOfRevenue"],
            diluted_average_shares=yahooquery_serie["DilutedAverageShares"],
            diluted_eps=yahooquery_serie["DilutedEPS"],
            diluted_ni_availto_com_stockholders=yahooquery_serie["DilutedNIAvailtoComStockholders"],
            ebit=yahooquery_serie["EBIT"],
            ebitda=yahooquery_serie["EBITDA"],
            gross_profit=yahooquery_serie["GrossProfit"],
            interest_expense=yahooquery_serie["InterestExpense"],
            interest_expense_non_operating=yahooquery_serie["InterestExpenseNonOperating"],
            interest_income=yahooquery_serie["InterestIncome"],
            interest_income_non_operating=yahooquery_serie["InterestIncomeNonOperating"],
            net_income=yahooquery_serie["NetIncome"],
            net_income_common_stockholders=yahooquery_serie["NetIncomeCommonStockholders"],
            net_income_continuous_operations=yahooquery_serie["NetIncomeContinuousOperations"],
            net_income_from_continuing_and_discontinued_operation=yahooquery_serie["NetIncomeFromContinuingAndDiscontinuedOperation"],
            net_income_from_continuing_operation_net_minority_interest=yahooquery_serie["NetIncomeFromContinuingOperationNetMinorityInterest"],
            net_income_including_noncontrolling_interests=yahooquery_serie["NetIncomeIncludingNoncontrollingInterests"],
            net_interest_income=yahooquery_serie["NetInterestIncome"],
            net_non_operating_interest_income_expense=yahooquery_serie["NetNonOperatingInterestIncomeExpense"],
            normalized_ebitda=yahooquery_serie["NormalizedEBITDA"],
            normalized_income=yahooquery_serie["NormalizedIncome"],
            operating_expense=yahooquery_serie["OperatingExpense"],
            operating_income=yahooquery_serie["OperatingIncome"],
            operating_revenue=yahooquery_serie["OperatingRevenue"],
            other_income_expense=yahooquery_serie["OtherIncomeExpense"],
            other_non_operating_income_expenses=yahooquery_serie["OtherNonOperatingIncomeExpenses"],
            pretax_income=yahooquery_serie["PretaxIncome"],
            reconciled_cost_of_revenue=yahooquery_serie["ReconciledCostOfRevenue"],
            reconciled_depreciation=yahooquery_serie["ReconciledDepreciation"],
            research_and_development=yahooquery_serie["ResearchAndDevelopment"],
            selling_general_and_administration=yahooquery_serie["SellingGeneralAndAdministration"],
            tax_effect_of_unusual_items=yahooquery_serie["TaxEffectOfUnusualItems"],
            tax_provision=yahooquery_serie["TaxProvision"],
            tax_rate_for_calcs=yahooquery_serie["TaxRateForCalcs"],
            total_expenses=yahooquery_serie["TotalExpenses"],
            total_operating_income_as_reported=yahooquery_serie["TotalOperatingIncomeAsReported"],
            total_revenue=yahooquery_serie["TotalRevenue"]
        )

    def normalize_institutional_yahooquery(self):
        df = self.yq_company.institution_ownership
        df = df.reset_index()
        df = df.drop(columns=['symbol','row','maxAge'])
        return df

    def normalize_key_stats_yahooquery(self, key_stats):
        last_fiscal_year_end = key_stats.get('lastFiscalYearEnd')
        next_fiscal_year_end = key_stats.get('nextFiscalYearEnd')
        most_recent_quarter = key_stats.get('mostRecentQuarter')
        if last_fiscal_year_end:
            last_fiscal_year_end=datetime.datetime.strptime(last_fiscal_year_end, '%y/%m/%d')
        if next_fiscal_year_end:
            next_fiscal_year_end=datetime.datetime.strptime(next_fiscal_year_end, '%y/%m/%d')
        if most_recent_quarter:
            most_recent_quarter=datetime.datetime.strptime(most_recent_quarter, '%y/%m/%d')
        return dict(
            date=datetime.datetime.now().year,
            year=datetime.datetime.now().date(),
            company=self.company,
            max_age=key_stats.get('maxAge'),
            price_hint=key_stats.get('priceHint'),
            enterprise_value=key_stats.get('enterpriseValue'),
            forward_pe=key_stats.get('forwardPE'),
            profit_margins=key_stats.get('profitMargins'),
            float_shares=key_stats.get('floatShares'),
            shares_outstanding=key_stats.get('sharesOutstanding'),
            shares_short=key_stats.get('sharesShort'),
            shares_short_prior_month=key_stats.get('sharesShortPriorMonth'),
            shares_short_previous_month_date=key_stats.get('sharesShortPreviousMonthDate'),
            date_short_interest=key_stats.get('dateShortInterest'),
            shares_percent_shares_out=key_stats.get('sharesPercentSharesOut'),
            held_percent_insiders=key_stats.get('heldPercentInsiders'),
            held_percent_institutions=key_stats.get('heldPercentInstitutions'),
            short_ratio=key_stats.get('shortRatio'),
            short_percent_of_float=key_stats.get('shortPercentOfFloat'),
            beta=key_stats.get('beta'),
            category=key_stats.get('category'),
            book_value=key_stats.get('bookValue'),
            price_to_book=key_stats.get('priceToBook'),
            fund_family=key_stats.get('fundFamily'),
            legal_type=key_stats.get('legalType'),
            last_fiscal_year_end=last_fiscal_year_end,
            next_fiscal_year_end=next_fiscal_year_end,
            most_recent_quarter=most_recent_quarter,
            earnings_quarterly_growth=key_stats.get('earningsQuarterlyGrowth'),
            net_income_to_common=key_stats.get('netIncomeToCommon'),
            trailing_eps=key_stats.get('trailingEps'),
            forward_eps=key_stats.get('forwardEps'),
            peg_ratio=key_stats.get('pegRatio'),
            last_split_factor=key_stats.get('lastSplitFactor'),
            last_split_date=key_stats.get('lastSplitDate'),
            enterprise_to_revenue=key_stats.get('enterpriseToRevenue'),
            enterprise_to_ebitda=key_stats.get('enterpriseToEbitda'),
            week_change_52=key_stats.get('52WeekChange'),
            sand_p52_week_change=key_stats.get('SandP52WeekChange'),
        )
