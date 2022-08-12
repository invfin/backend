from typing import Dict, Union, Any

from apps.general.models import Currency


class NormalizeFinprep:
    def create_income_statement(
        self,
        inc_stt: Dict[str, Union[float, int, str, Any]]
    ) -> Dict[str, Union[float, int, str, Any]]:
        return dict(
            date=inc_stt['calendarYear'],
            year=inc_stt['date'],
            reported_currency=Currency.objects.get_or_create(
                currency=inc_stt['reportedCurrency']
            )[0],
            revenue=inc_stt['revenue'],
            cost_of_revenue=inc_stt['costOfRevenue'],
            gross_profit=inc_stt['grossProfit'],
            rd_expenses=inc_stt['researchAndDevelopmentExpenses'],
            general_administrative_expenses=inc_stt['generalAndAdministrativeExpenses'],
            selling_marketing_expenses=inc_stt['sellingAndMarketingExpenses'],
            sga_expenses=inc_stt['sellingGeneralAndAdministrativeExpenses'],
            other_expenses=inc_stt['otherExpenses'],
            operating_expenses=inc_stt['operatingExpenses'],
            cost_and_expenses=inc_stt['costAndExpenses'],
            interest_expense=inc_stt['interestExpense'],
            depreciation_amortization=inc_stt['depreciationAndAmortization'],
            ebitda=inc_stt['ebitda'],
            operating_income=inc_stt['operatingIncome'],
            net_total_other_income_expenses=inc_stt['totalOtherIncomeExpensesNet'],
            income_before_tax=inc_stt['incomeBeforeTax'],
            income_tax_expenses=inc_stt['incomeTaxExpense'],
            net_income=inc_stt['netIncome'],
            weighted_average_shares_outstanding=inc_stt['weightedAverageShsOut'],
            weighted_average_diluated_shares_outstanding=inc_stt['weightedAverageShsOutDil']
        )

    def create_balance_sheet_dict(
        self,
        bal_sht: Dict[str, Union[float, int, str, Any]]
    ) -> Dict[str, Union[float, int, str, Any]]:
        return dict(
            date=bal_sht['calendarYear'],
            year=bal_sht['date'],
            reported_currency=Currency.objects.get_or_create(
                currency=bal_sht['reportedCurrency']
            )[0],
            cash_and_cash_equivalents=bal_sht['cashAndCashEquivalents'],
            short_term_investments=bal_sht['shortTermInvestments'],
            cash_and_short_term_investements=bal_sht['cashAndShortTermInvestments'],
            net_receivables=bal_sht['netReceivables'],
            inventory=bal_sht['inventory'],
            other_current_assets=bal_sht['otherCurrentAssets'],
            total_current_assets=bal_sht['totalCurrentAssets'],
            property_plant_equipement=bal_sht['propertyPlantEquipmentNet'],
            goodwill=bal_sht['goodwill'],
            intangible_assets=bal_sht['intangibleAssets'],
            goodwill_and_intangible_assets=bal_sht['goodwillAndIntangibleAssets'],
            long_term_investments=bal_sht['longTermInvestments'],
            tax_assets=bal_sht['taxAssets'],
            other_non_current_assets=bal_sht['otherNonCurrentAssets'],
            total_non_current_assets=bal_sht['totalNonCurrentAssets'],
            other_assets=bal_sht['otherAssets'],
            total_assets=bal_sht['totalAssets'],
            account_payables=bal_sht['accountPayables'],
            short_term_debt=bal_sht['short_term_debt'],
            tax_payables=bal_sht['tax_payables'],
            deferred_revenue=bal_sht['deferred_revenue'],
            other_current_liabilities=bal_sht['otherCurrentLiabilities'],
            total_current_liabilities=bal_sht['totalCurrentLiabilities'],
            long_term_debt=bal_sht['longTermDebt'],
            deferred_revenue_non_current=bal_sht['deferred_revenueNonCurrent'],
            deferred_tax_liabilities_non_current=bal_sht['deferredTaxLiabilitiesNonCurrent'],
            other_non_current_liabilities=bal_sht['otherNonCurrentLiabilities'],
            total_non_current_liabilities=bal_sht['totalNonCurrentLiabilities'],
            other_liabilities=bal_sht['otherLiabilities'],
            total_liabilities=bal_sht['totalLiabilities'],
            common_stocks=bal_sht['commonStock'],
            retained_earnings=bal_sht['retainedEarnings'],
            accumulated_other_comprehensive_income_loss=bal_sht[
                'accumulatedOtherComprehensiveIncomeLoss'
            ],
            othertotal_stockholders_equity=bal_sht['othertotalStockholdersEquity'],
            total_stockholders_equity=bal_sht['totalStockholdersEquity'],
            total_liabilities_and_stockholders_equity=bal_sht[
                'totalLiabilitiesAndStockholdersEquity'
            ],
            total_investments=bal_sht['totalInvestments'],
            total_debt=bal_sht['totalDebt'],
            net_debt=bal_sht['netDebt'],
        )

    def create_cashflow_statement_dict(
        self,
        csf_stt: Dict[str, Union[float, int, str, Any]]
    ) -> Dict[str, Union[float, int, str, Any]]:
        return dict(
            date=csf_stt['calendarYear'],
            year=csf_stt['date'],
            reported_currency=Currency.objects.get_or_create(
                currency=csf_stt['reportedCurrency']
            )[0],
            net_income=csf_stt['netIncome'],
            depreciation_amortization=csf_stt['depreciationAndAmortization'],
            deferred_income_tax=csf_stt['deferredIncomeTax'],
            stock_based_compesation=csf_stt['stockBasedCompensation'],
            change_in_working_capital=csf_stt['changeInWorkingCapital'],
            accounts_receivables=csf_stt['accountsReceivables'],
            inventory=csf_stt['inventory'],
            accounts_payable=csf_stt['accountsPayables'],
            other_working_capital=csf_stt['otherWorkingCapital'],
            other_non_cash_items=csf_stt['otherNonCashItems'],
            operating_activities_cf=csf_stt['netCashProvidedByOperatingActivities'],
            investments_property_plant_equipment=csf_stt['investmentsInPropertyPlantAndEquipment'],
            acquisitions_net=csf_stt['acquisitionsNet'],
            purchases_investments=csf_stt['purchasesOfInvestments'],
            sales_maturities_investments=csf_stt['salesMaturitiesOfInvestments'],
            other_investing_activites=csf_stt['otherInvestingActivites'],
            investing_activities_cf=csf_stt['netCashUsedForInvestingActivites'],
            debt_repayment=csf_stt['debtRepayment'],
            common_stock_issued=csf_stt['commonStockIssued'],
            common_stock_repurchased=csf_stt['commonStockRepurchased'],
            dividends_paid=csf_stt['dividendsPaid'],
            other_financing_activities=csf_stt['otherFinancingActivites'],
            financing_activities_cf=csf_stt['netCashUsedProvidedByFinancingActivities'],
            effect_forex_exchange=csf_stt['effectOfForexChangesOnCash'],
            net_change_cash=csf_stt['netChangeInCash'],
            cash_end_period=csf_stt['cashAtEndOfPeriod'],
            cash_beginning_period=csf_stt['cashAtBeginningOfPeriod'],
            operating_cf=csf_stt['operatingCashFlow'],
            capex=csf_stt['capitalExpenditure'],
            fcf=csf_stt['freeCashFlow'],
        )
