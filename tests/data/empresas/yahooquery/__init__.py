from typing import List
import pandas as pd


def list_to_dataframe(data:List)->pd.DataFrame:
    df = pd.DataFrame.from_dict({(ind, "AAPL"): dic for ind, dic in enumerate(data)}, orient='index', columns=[
        'asOfDate',
        'periodType', 'currencyCode', 'BasicAverageShares', 'BasicEPS', 'CostOfRevenue',
        'DilutedAverageShares', 'DilutedEPS', 'DilutedNIAvailtoComStockholders', 'EBIT',
        'ReconciledCostOfRevenue', 'ReconciledDepreciation', 'ResearchAndDevelopment',
        'SellingGeneralAndAdministration', 'TaxEffectOfUnusualItems', 'TaxProvision',
        'TaxRateForCalcs', 'TotalExpenses', 'TotalOperatingIncomeAsReported', 'TotalRevenue',
    ],)
    df.index.names = ["index", 'symbol']
    df = df.droplevel(0)
    return df
