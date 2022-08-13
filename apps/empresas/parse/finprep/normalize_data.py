from typing import Dict, Union, Any

from apps.general.constants import PERIOD_FOR_YEAR
from apps.general.models import Currency


class NormalizeFinprep:
    def create_income_statement_finprep(
        self,
        finprep_dict: Dict[str, Union[float, int, str, Any]]
    ) -> Dict[str, Union[float, int, str, Any]]:
        return dict(
            accepted_date=finprep_dict["acceptedDate"],
            ebitdaratio=finprep_dict["ebitdaratio"],
            eps=finprep_dict["eps"],
            epsdiluted=finprep_dict["epsdiluted"],
            filling_date=finprep_dict["fillingDate"],
            final_link=finprep_dict["finalLink"],
            gross_profit_ratio=finprep_dict["grossProfitRatio"],
            income_before_tax_ratio=finprep_dict["incomeBeforeTaxRatio"],
            link=finprep_dict["link"],
            net_income_ratio=finprep_dict["netIncomeRatio"],
            operating_income_ratio=finprep_dict["operatingIncomeRatio"],
            period=PERIOD_FOR_YEAR,
            reported_currency=finprep_dict["reportedCurrency"],
            date=finprep_dict['calendarYear'],
            year=finprep_dict['date'],
            reported_currency=Currency.objects.get_or_create(
                currency=finprep_dict['reportedCurrency']
            )[0],
            revenue=finprep_dict['revenue'],
            cost_of_revenue=finprep_dict['costOfRevenue'],
            gross_profit=finprep_dict['grossProfit'],
            rd_expenses=finprep_dict['researchAndDevelopmentExpenses'],
            general_administrative_expenses=finprep_dict['generalAndAdministrativeExpenses'],
            selling_marketing_expenses=finprep_dict['sellingAndMarketingExpenses'],
            sga_expenses=finprep_dict['sellingGeneralAndAdministrativeExpenses'],
            other_expenses=finprep_dict['otherExpenses'],
            operating_expenses=finprep_dict['operatingExpenses'],
            cost_and_expenses=finprep_dict['costAndExpenses'],
            interest_expense=finprep_dict['interestExpense'],
            depreciation_amortization=finprep_dict['depreciationAndAmortization'],
            ebitda=finprep_dict['ebitda'],
            operating_income=finprep_dict['operatingIncome'],
            net_total_other_income_expenses=finprep_dict['totalOtherIncomeExpensesNet'],
            income_before_tax=finprep_dict['incomeBeforeTax'],
            income_tax_expenses=finprep_dict['incomeTaxExpense'],
            net_income=finprep_dict['netIncome'],
            weighted_average_shares_outstanding=finprep_dict['weightedAverageShsOut'],
            weighted_average_diluated_shares_outstanding=finprep_dict['weightedAverageShsOutDil']
        )

    def create_balance_sheet_finprep(
        self,
        finprep_dict: Dict[str, Union[float, int, str, Any]]
    ) -> Dict[str, Union[float, int, str, Any]]:
        return dict(
            accepted_date=finprep_dict["acceptedDate"],
            filling_date=finprep_dict["fillingDate"],
            final_link=finprep_dict["finalLink"],
            link=finprep_dict["link"],
            period=PERIOD_FOR_YEAR,
            date=finprep_dict['calendarYear'],
            year=finprep_dict['date'],
            reported_currency=Currency.objects.get_or_create(
                currency=finprep_dict['reportedCurrency']
            )[0],
            account_payables=['accountPayables'],
            accumulated_other_comprehensive_income_loss=['accumulatedOtherComprehensiveIncomeLoss'],
            capital_lease_obligations=['capitalLeaseObligations'],
            cash_and_cash_equivalents=['cashAndCashEquivalents'],
            cash_and_short_term_investments=['cashAndShortTermInvestments'],
            common_stocks=['commonStock'],
            deferred_revenue=['deferredRevenue'],
            deferred_revenue_non_current=['deferredRevenueNonCurrent'],
            deferred_tax_liabilities_non_current=['deferredTaxLiabilitiesNonCurrent'],
            goodwill=['goodwill'],
            goodwill_and_intangible_assets=['goodwillAndIntangibleAssets'],
            intangible_assets=['intangibleAssets'],
            inventory=['inventory'],
            long_term_debt=['longTermDebt'],
            long_term_investments=['longTermInvestments'],
            minority_interest=['minorityInterest'],
            net_debt=['netDebt'],
            net_receivables=['netReceivables'],
            other_assets=['otherAssets'],
            other_current_assets=['otherCurrentAssets'],
            other_current_liabilities=['otherCurrentLiabilities'],
            other_liabilities=['otherLiabilities'],
            other_non_current_assets=['otherNonCurrentAssets'],
            other_non_current_liabilities=['otherNonCurrentLiabilities'],
            othertotal_stockholders_equity=['othertotalStockholdersEquity'],
            preferred_stock=['preferredStock'],
            property_plant_equipment_net=['propertyPlantEquipmentNet'],
            reported_currency=['reportedCurrency'],
            retained_earnings=['retainedEarnings'],
            short_term_debt=['shortTermDebt'],
            short_term_investments=['shortTermInvestments'],
            tax_assets=['taxAssets'],
            tax_payables=['taxPayables'],
            total_assets=['totalAssets'],
            total_current_assets=['totalCurrentAssets'],
            total_current_liabilities=['totalCurrentLiabilities'],
            total_debt=['totalDebt'],
            total_equity=['totalEquity'],
            total_investments=['totalInvestments'],
            total_liabilities=['totalLiabilities'],
            total_liabilities_and_stockholders_equity=['totalLiabilitiesAndStockholdersEquity'],
            total_liabilities_and_total_equity=['totalLiabilitiesAndTotalEquity'],
            total_non_current_assets=['totalNonCurrentAssets'],
            total_non_current_liabilities=['totalNonCurrentLiabilities'],
            total_stockholders_equity=['totalStockholdersEquity']
        )

    def create_cashflow_statement_finprep(
        self,
        finprep_dict: Dict[str, Union[float, int, str, Any]]
    ) -> Dict[str, Union[float, int, str, Any]]:
        return dict(
            accepted_date=finprep_dict["acceptedDate"],
            filling_date=finprep_dict["fillingDate"],
            final_link=finprep_dict["finalLink"],
            link=finprep_dict["link"],
            period=PERIOD_FOR_YEAR,
            date=finprep_dict['calendarYear'],
            year=finprep_dict['date'],
            reported_currency=Currency.objects.get_or_create(
                currency=finprep_dict['reportedCurrency']
            )[0],
            net_income=finprep_dict['netIncome'],
            depreciation_amortization=finprep_dict['depreciationAndAmortization'],
            deferred_income_tax=finprep_dict['deferredIncomeTax'],
            stock_based_compesation=finprep_dict['stockBasedCompensation'],
            change_in_working_capital=finprep_dict['changeInWorkingCapital'],
            accounts_receivables=finprep_dict['accountsReceivables'],
            inventory=finprep_dict['inventory'],
            accounts_payable=finprep_dict['accountsPayables'],
            other_working_capital=finprep_dict['otherWorkingCapital'],
            other_non_cash_items=finprep_dict['otherNonCashItems'],
            operating_activities_cf=finprep_dict['netCashProvidedByOperatingActivities'],
            investments_property_plant_equipment=finprep_dict['investmentsInPropertyPlantAndEquipment'],
            acquisitions_net=finprep_dict['acquisitionsNet'],
            purchases_investments=finprep_dict['purchasesOfInvestments'],
            sales_maturities_investments=finprep_dict['salesMaturitiesOfInvestments'],
            other_investing_activites=finprep_dict['otherInvestingActivites'],
            investing_activities_cf=finprep_dict['netCashUsedForInvestingActivites'],
            debt_repayment=finprep_dict['debtRepayment'],
            common_stock_issued=finprep_dict['commonStockIssued'],
            common_stock_repurchased=finprep_dict['commonStockRepurchased'],
            dividends_paid=finprep_dict['dividendsPaid'],
            other_financing_activities=finprep_dict['otherFinancingActivites'],
            financing_activities_cf=finprep_dict['netCashUsedProvidedByFinancingActivities'],
            effect_forex_exchange=finprep_dict['effectOfForexChangesOnCash'],
            net_change_cash=finprep_dict['netChangeInCash'],
            cash_end_period=finprep_dict['cashAtEndOfPeriod'],
            cash_beginning_period=finprep_dict['cashAtBeginningOfPeriod'],
            operating_cf=finprep_dict['operatingCashFlow'],
            capex=finprep_dict['capitalExpenditure'],
            fcf=finprep_dict['freeCashFlow'],
        )




