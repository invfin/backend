from typing import Any, Dict, Union

from src.currencies.models import Currency
from src.periods.models import Period


class NormalizeFinprep:
    company = None

    def initial_data(
        self, finprep_dict: Dict[str, Union[float, int, str, Any]]
    ) -> Dict[str, Union[float, int, str, Any]]:
        return dict(
            date=finprep_dict["calendarYear"],
            year=finprep_dict["date"],
            company=self.company,
            period=Period.objects.for_year_period(finprep_dict["calendarYear"]),
            reported_currency=Currency.objects.financial_currency(finprep_dict["reportedCurrency"]),
            accepted_date=finprep_dict["acceptedDate"],
            filling_date=finprep_dict["fillingDate"],
            final_link=finprep_dict["finalLink"],
            link=finprep_dict["link"],
        )

    def normalize_income_statements_finprep(
        self, finprep_dict: Dict[str, Union[float, int, str, Any]]
    ) -> Dict[str, Union[float, int, str, Any]]:
        return dict(
            self.initial_data(finprep_dict),
            calendar_year=finprep_dict["calendarYear"],
            cik=finprep_dict["cik"],
            cost_and_expenses=finprep_dict["costAndExpenses"],
            cost_of_revenue=finprep_dict["costOfRevenue"],
            depreciation_and_amortization=finprep_dict["depreciationAndAmortization"],
            ebitda=finprep_dict["ebitda"],
            ebitdaratio=finprep_dict["ebitdaratio"],
            eps=finprep_dict["eps"],
            epsdiluted=finprep_dict["epsdiluted"],
            general_and_administrative_expenses=finprep_dict["generalAndAdministrativeExpenses"],
            gross_profit=finprep_dict["grossProfit"],
            gross_profit_ratio=finprep_dict["grossProfitRatio"],
            income_before_tax=finprep_dict["incomeBeforeTax"],
            income_before_tax_ratio=finprep_dict["incomeBeforeTaxRatio"],
            income_tax_expense=finprep_dict["incomeTaxExpense"],
            interest_expense=finprep_dict["interestExpense"],
            interest_income=finprep_dict["interestIncome"],
            net_income=finprep_dict["netIncome"],
            net_income_ratio=finprep_dict["netIncomeRatio"],
            operating_expenses=finprep_dict["operatingExpenses"],
            operating_income=finprep_dict["operatingIncome"],
            operating_income_ratio=finprep_dict["operatingIncomeRatio"],
            other_expenses=finprep_dict["otherExpenses"],
            research_and_development_expenses=finprep_dict["researchAndDevelopmentExpenses"],
            revenue=finprep_dict["revenue"],
            selling_and_marketing_expenses=finprep_dict["sellingAndMarketingExpenses"],
            selling_general_and_administrative_expenses=finprep_dict["sellingGeneralAndAdministrativeExpenses"],
            symbol=finprep_dict["symbol"],
            total_other_income_expenses_net=finprep_dict["totalOtherIncomeExpensesNet"],
            weighted_average_shs_out=finprep_dict["weightedAverageShsOut"],
            weighted_average_shs_out_dil=finprep_dict["weightedAverageShsOutDil"],
        )

    def normalize_balance_sheets_finprep(
        self, finprep_dict: Dict[str, Union[float, int, str, Any]]
    ) -> Dict[str, Union[float, int, str, Any]]:
        return dict(
            self.initial_data(finprep_dict),
            account_payables=finprep_dict["accountPayables"],
            accumulated_other_comprehensive_income_loss=finprep_dict["accumulatedOtherComprehensiveIncomeLoss"],
            calendar_year=finprep_dict["calendarYear"],
            capital_lease_obligations=finprep_dict["capitalLeaseObligations"],
            cash_and_cash_equivalents=finprep_dict["cashAndCashEquivalents"],
            cash_and_short_term_investments=finprep_dict["cashAndShortTermInvestments"],
            cik=finprep_dict["cik"],
            common_stock=finprep_dict["commonStock"],
            deferred_revenue=finprep_dict["deferredRevenue"],
            deferred_revenue_non_current=finprep_dict["deferredRevenueNonCurrent"],
            deferred_tax_liabilities_non_current=finprep_dict["deferredTaxLiabilitiesNonCurrent"],
            goodwill=finprep_dict["goodwill"],
            goodwill_and_intangible_assets=finprep_dict["goodwillAndIntangibleAssets"],
            intangible_assets=finprep_dict["intangibleAssets"],
            inventory=finprep_dict["inventory"],
            long_term_debt=finprep_dict["longTermDebt"],
            long_term_investments=finprep_dict["longTermInvestments"],
            minority_interest=finprep_dict["minorityInterest"],
            net_debt=finprep_dict["netDebt"],
            net_receivables=finprep_dict["netReceivables"],
            other_assets=finprep_dict["otherAssets"],
            other_current_assets=finprep_dict["otherCurrentAssets"],
            other_current_liabilities=finprep_dict["otherCurrentLiabilities"],
            other_liabilities=finprep_dict["otherLiabilities"],
            other_non_current_assets=finprep_dict["otherNonCurrentAssets"],
            other_non_current_liabilities=finprep_dict["otherNonCurrentLiabilities"],
            othertotal_stockholders_equity=finprep_dict["othertotalStockholdersEquity"],
            preferred_stock=finprep_dict["preferredStock"],
            property_plant_equipment_net=finprep_dict["propertyPlantEquipmentNet"],
            retained_earnings=finprep_dict["retainedEarnings"],
            short_term_debt=finprep_dict["shortTermDebt"],
            short_term_investments=finprep_dict["shortTermInvestments"],
            symbol=finprep_dict["symbol"],
            tax_assets=finprep_dict["taxAssets"],
            tax_payables=finprep_dict["taxPayables"],
            total_assets=finprep_dict["totalAssets"],
            total_current_assets=finprep_dict["totalCurrentAssets"],
            total_current_liabilities=finprep_dict["totalCurrentLiabilities"],
            total_debt=finprep_dict["totalDebt"],
            total_equity=finprep_dict["totalEquity"],
            total_investments=finprep_dict["totalInvestments"],
            total_liabilities=finprep_dict["totalLiabilities"],
            total_liabilities_and_stockholders_equity=finprep_dict["totalLiabilitiesAndStockholdersEquity"],
            total_liabilities_and_total_equity=finprep_dict["totalLiabilitiesAndTotalEquity"],
            total_non_current_assets=finprep_dict["totalNonCurrentAssets"],
            total_non_current_liabilities=finprep_dict["totalNonCurrentLiabilities"],
            total_stockholders_equity=finprep_dict["totalStockholdersEquity"],
        )

    def normalize_cashflow_statements_finprep(
        self, finprep_dict: Dict[str, Union[float, int, str, Any]]
    ) -> Dict[str, Union[float, int, str, Any]]:
        return dict(
            self.initial_data(finprep_dict),
            accounts_payables=finprep_dict["accountsPayables"],
            accounts_receivables=finprep_dict["accountsReceivables"],
            acquisitions_net=finprep_dict["acquisitionsNet"],
            calendar_year=finprep_dict["calendarYear"],
            capital_expenditure=finprep_dict["capitalExpenditure"],
            cash_at_beginning_of_period=finprep_dict["cashAtBeginningOfPeriod"],
            cash_at_end_of_period=finprep_dict["cashAtEndOfPeriod"],
            change_in_working_capital=finprep_dict["changeInWorkingCapital"],
            cik=finprep_dict["cik"],
            common_stock_issued=finprep_dict["commonStockIssued"],
            common_stock_repurchased=finprep_dict["commonStockRepurchased"],
            debt_repayment=finprep_dict["debtRepayment"],
            deferred_income_tax=finprep_dict["deferredIncomeTax"],
            depreciation_and_amortization=finprep_dict["depreciationAndAmortization"],
            dividends_paid=finprep_dict["dividendsPaid"],
            effect_of_forex_changes_on_cash=finprep_dict["effectOfForexChangesOnCash"],
            free_cash_flow=finprep_dict["freeCashFlow"],
            inventory=finprep_dict["inventory"],
            investments_in_property_plant_and_equipment=finprep_dict["investmentsInPropertyPlantAndEquipment"],
            net_cash_provided_by_operating_activities=finprep_dict["netCashProvidedByOperatingActivities"],
            net_cash_used_for_investing_activites=finprep_dict["netCashUsedForInvestingActivites"],
            net_cash_used_provided_by_financing_activities=finprep_dict["netCashUsedProvidedByFinancingActivities"],
            net_change_in_cash=finprep_dict["netChangeInCash"],
            net_income=finprep_dict["netIncome"],
            operating_cash_flow=finprep_dict["operatingCashFlow"],
            other_financing_activites=finprep_dict["otherFinancingActivites"],
            other_investing_activites=finprep_dict["otherInvestingActivites"],
            other_non_cash_items=finprep_dict["otherNonCashItems"],
            other_working_capital=finprep_dict["otherWorkingCapital"],
            purchases_of_investments=finprep_dict["purchasesOfInvestments"],
            sales_maturities_of_investments=finprep_dict["salesMaturitiesOfInvestments"],
            stock_based_compensation=finprep_dict["stockBasedCompensation"],
            symbol=finprep_dict["symbol"],
        )
