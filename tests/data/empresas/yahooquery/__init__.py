from typing import List
import pandas as pd

income_statement_columns = [
        'asOfDate',
        'periodType', 'currencyCode', 'BasicAverageShares', 'BasicEPS', 'CostOfRevenue',
        'DilutedAverageShares', 'DilutedEPS', 'DilutedNIAvailtoComStockholders', 'EBIT',
        'ReconciledCostOfRevenue', 'ReconciledDepreciation', 'ResearchAndDevelopment',
        'SellingGeneralAndAdministration', 'TaxEffectOfUnusualItems', 'TaxProvision',
        'TaxRateForCalcs', 'TotalExpenses', 'TotalOperatingIncomeAsReported', 'TotalRevenue',
    ]

balance_sheet_columns = ['asOfDate', 'periodType', 'currencyCode', 'AccountsPayable',
       'AccountsReceivable', 'AccumulatedDepreciation',
       'AvailableForSaleSecurities', 'CapitalStock', 'CashAndCashEquivalents',
       'CashCashEquivalentsAndShortTermInvestments', 'CashEquivalents',
       'CashFinancial', 'CommercialPaper', 'CommonStock', 'CommonStockEquity',
       'CurrentAssets', 'CurrentDebt', 'CurrentDebtAndCapitalLeaseObligation',
       'CurrentDeferredLiabilities', 'CurrentDeferredRevenue',
       'CurrentLiabilities', 'FinishedGoods',
       'GainsLossesNotAffectingRetainedEarnings', 'GrossPPE', 'Inventory',
       'InvestedCapital', 'InvestmentinFinancialAssets',
       'InvestmentsAndAdvances', 'LandAndImprovements', 'Leases',
       'LongTermDebt', 'LongTermDebtAndCapitalLeaseObligation',
       'MachineryFurnitureEquipment', 'NetDebt', 'NetPPE', 'NetTangibleAssets',
       'OrdinarySharesNumber', 'OtherCurrentAssets', 'OtherCurrentBorrowings',
       'OtherCurrentLiabilities', 'OtherInvestments', 'OtherNonCurrentAssets',
       'OtherNonCurrentLiabilities', 'OtherReceivables',
       'OtherShortTermInvestments', 'Payables', 'PayablesAndAccruedExpenses',
       'Properties', 'RawMaterials', 'Receivables', 'RetainedEarnings',
       'ShareIssued', 'StockholdersEquity', 'TangibleBookValue', 'TotalAssets',
       'TotalCapitalization', 'TotalDebt', 'TotalEquityGrossMinorityInterest',
       'TotalLiabilitiesNetMinorityInterest', 'TotalNonCurrentAssets',
       'TotalNonCurrentLiabilitiesNetMinorityInterest',
       'TradeandOtherPayablesNonCurrent', 'WorkingCapital',]

chasflow_columns = ['asOfDate', 'periodType', 'currencyCode', 'BeginningCashPosition',
       'CapitalExpenditure', 'CashDividendsPaid',
       'CashFlowFromContinuingFinancingActivities',
       'CashFlowFromContinuingInvestingActivities',
       'CashFlowFromContinuingOperatingActivities', 'ChangeInAccountPayable',
       'ChangeInCashSupplementalAsReported', 'ChangeInInventory',
       'ChangeInOtherCurrentAssets', 'ChangeInOtherCurrentLiabilities',
       'ChangeInOtherWorkingCapital', 'ChangeInPayable',
       'ChangeInPayablesAndAccruedExpense', 'ChangeInReceivables',
       'ChangeInWorkingCapital', 'ChangesInAccountReceivables',
       'ChangesInCash', 'CommonStockDividendPaid', 'CommonStockPayments',
       'DeferredIncomeTax', 'DeferredTax', 'DepreciationAmortizationDepletion',
       'DepreciationAndAmortization', 'EndCashPosition', 'FinancingCashFlow',
       'FreeCashFlow', 'IncomeTaxPaidSupplementalData',
       'InterestPaidSupplementalData', 'InvestingCashFlow', 'IssuanceOfDebt',
       'LongTermDebtIssuance', 'LongTermDebtPayments',
       'NetBusinessPurchaseAndSale', 'NetCommonStockIssuance', 'NetIncome',
       'NetIncomeFromContinuingOperations', 'NetInvestmentPurchaseAndSale',
       'NetIssuancePaymentsOfDebt', 'NetLongTermDebtIssuance',
       'NetOtherFinancingCharges', 'NetOtherInvestingChanges',
       'NetPPEPurchaseAndSale', 'NetShortTermDebtIssuance',
       'OperatingCashFlow', 'OtherNonCashItems', 'PurchaseOfBusiness',
       'PurchaseOfInvestment', 'PurchaseOfPPE', 'RepaymentOfDebt',
       'RepurchaseOfCapitalStock', 'SaleOfInvestment', 'ShortTermDebtIssuance',
       'ShortTermDebtPayments', 'StockBasedCompensation',]
def list_to_dataframe(data:List, columns:List[str])->pd.DataFrame:
    df = pd.DataFrame.from_dict({(ind, "AAPL"): dic for ind, dic in enumerate(data)}, orient='index', columns=columns,)
    df.index.names = ["index", 'symbol']
    df = df.droplevel(0)
    return df
