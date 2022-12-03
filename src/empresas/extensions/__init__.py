CASHFLOW = {
    "financing_activities_cf": {"yahooquery": "purchase_of_ppe", "yfinance": "capital_expenditures"},
    "capex": {
        "yahooquery": "purchase_of_ppe",
    },
    "net_income": {"yahooquery": "financing_cash_flow", "yfinance": "total_cash_from_financing_activities"},
    "net_change_cash": {"yahooquery": "financing_cash_flow", "yfinance": "total_cash_from_financing_activities"},
    "investments_property_plant_equipment": {
        "yahooquery": "investing_cash_flow",
        "yfinance": "total_cashflows_from_investing_activities",
    },
    "investing_activities_cf": {
        "yahooquery": "operating_cash_flow",
        "yfinance": "total_cash_from_operating_activities",
    },
    "operating_cf": {"yahooquery": "operating_cash_flow", "yfinance": "total_cash_from_operating_activities"},
    "operating_activities_cf": {"yahooquery": "net_income_from_continuing_operations", "yfinance": "net_income"},
}
