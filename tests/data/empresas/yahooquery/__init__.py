from typing import List

import pandas as pd

from .balance_sheet import yearly_balance_sheet
from .cashflow_statement import yearly_cashflow
from .income_statement import yearly_income

income_statement_columns = [
    "asOfDate",
    "periodType",
    "currencyCode",
    "BasicAverageShares",
    "BasicEPS",
    "CostOfRevenue",
    "DilutedAverageShares",
    "DilutedEPS",
    "DilutedNIAvailtoComStockholders",
    "EBIT",
    "ReconciledCostOfRevenue",
    "ReconciledDepreciation",
    "ResearchAndDevelopment",
    "SellingGeneralAndAdministration",
    "TaxEffectOfUnusualItems",
    "TaxProvision",
    "TaxRateForCalcs",
    "TotalExpenses",
    "TotalOperatingIncomeAsReported",
    "TotalRevenue",
]

balance_sheet_columns = [
    "asOfDate",
    "periodType",
    "currencyCode",
    "AccountsPayable",
    "AccountsReceivable",
    "AccumulatedDepreciation",
    "AvailableForSaleSecurities",
    "CapitalStock",
    "CashAndCashEquivalents",
    "CashCashEquivalentsAndShortTermInvestments",
    "CashEquivalents",
    "CashFinancial",
    "CommercialPaper",
    "CommonStock",
    "CommonStockEquity",
    "CurrentAssets",
    "CurrentDebt",
    "CurrentDebtAndCapitalLeaseObligation",
    "CurrentDeferredLiabilities",
    "CurrentDeferredRevenue",
    "CurrentLiabilities",
    "FinishedGoods",
    "GainsLossesNotAffectingRetainedEarnings",
    "GrossPPE",
    "Inventory",
    "InvestedCapital",
    "InvestmentinFinancialAssets",
    "InvestmentsAndAdvances",
    "LandAndImprovements",
    "Leases",
    "LongTermDebt",
    "LongTermDebtAndCapitalLeaseObligation",
    "MachineryFurnitureEquipment",
    "NetDebt",
    "NetPPE",
    "NetTangibleAssets",
    "OrdinarySharesNumber",
    "OtherCurrentAssets",
    "OtherCurrentBorrowings",
    "OtherCurrentLiabilities",
    "OtherInvestments",
    "OtherNonCurrentAssets",
    "OtherNonCurrentLiabilities",
    "OtherReceivables",
    "OtherShortTermInvestments",
    "Payables",
    "PayablesAndAccruedExpenses",
    "Properties",
    "RawMaterials",
    "Receivables",
    "RetainedEarnings",
    "ShareIssued",
    "StockholdersEquity",
    "TangibleBookValue",
    "TotalAssets",
    "TotalCapitalization",
    "TotalDebt",
    "TotalEquityGrossMinorityInterest",
    "TotalLiabilitiesNetMinorityInterest",
    "TotalNonCurrentAssets",
    "TotalNonCurrentLiabilitiesNetMinorityInterest",
    "TradeandOtherPayablesNonCurrent",
    "WorkingCapital",
]

cashflow_columns = [
    "asOfDate",
    "periodType",
    "currencyCode",
    "BeginningCashPosition",
    "CapitalExpenditure",
    "CashDividendsPaid",
    "CashFlowFromContinuingFinancingActivities",
    "CashFlowFromContinuingInvestingActivities",
    "CashFlowFromContinuingOperatingActivities",
    "ChangeInAccountPayable",
    "ChangeInCashSupplementalAsReported",
    "ChangeInInventory",
    "ChangeInOtherCurrentAssets",
    "ChangeInOtherCurrentLiabilities",
    "ChangeInOtherWorkingCapital",
    "ChangeInPayable",
    "ChangeInPayablesAndAccruedExpense",
    "ChangeInReceivables",
    "ChangeInWorkingCapital",
    "ChangesInAccountReceivables",
    "ChangesInCash",
    "CommonStockDividendPaid",
    "CommonStockPayments",
    "DeferredIncomeTax",
    "DeferredTax",
    "DepreciationAmortizationDepletion",
    "DepreciationAndAmortization",
    "EndCashPosition",
    "FinancingCashFlow",
    "FreeCashFlow",
    "IncomeTaxPaidSupplementalData",
    "InterestPaidSupplementalData",
    "InvestingCashFlow",
    "IssuanceOfDebt",
    "LongTermDebtIssuance",
    "LongTermDebtPayments",
    "NetBusinessPurchaseAndSale",
    "NetCommonStockIssuance",
    "NetIncome",
    "NetIncomeFromContinuingOperations",
    "NetInvestmentPurchaseAndSale",
    "NetIssuancePaymentsOfDebt",
    "NetLongTermDebtIssuance",
    "NetOtherFinancingCharges",
    "NetOtherInvestingChanges",
    "NetPPEPurchaseAndSale",
    "NetShortTermDebtIssuance",
    "OperatingCashFlow",
    "OtherNonCashItems",
    "PurchaseOfBusiness",
    "PurchaseOfInvestment",
    "PurchaseOfPPE",
    "RepaymentOfDebt",
    "RepurchaseOfCapitalStock",
    "SaleOfInvestment",
    "ShortTermDebtIssuance",
    "ShortTermDebtPayments",
    "StockBasedCompensation",
]


def list_to_dataframe(data: List, columns: List[str]) -> pd.DataFrame:
    df = pd.DataFrame.from_dict(
        {(ind, "AAPL"): dic for ind, dic in enumerate(data)},
        orient="index",
        columns=columns,
    )
    df["asOfDate"] = [pd.Timestamp(value) for value in df["asOfDate"].values]
    df.index.names = ["index", "symbol"]
    df = df.droplevel(0)
    return df


def income_dataframe() -> pd.DataFrame:
    return list_to_dataframe(yearly_income, income_statement_columns)


def balance_dataframe() -> pd.DataFrame:
    return list_to_dataframe(yearly_balance_sheet, balance_sheet_columns)


def cashflow_dataframe() -> pd.DataFrame:
    return list_to_dataframe(yearly_cashflow, cashflow_columns)
