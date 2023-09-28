FINNHUB_BASE_URL = "https://finnhub.io/api/"
FINNHUB_API_VERSION = "v1"

FINPREP_BASE_URL = "https://financialmodelingprep.com/api/"

DATA_SOURCE_FINPREP = "finprep"
DATA_SOURCE_FINNHUB = "finnhub"
DATA_SOURCE_YFINANCE = "y_finance"
DATA_SOURCE_YAHOOQUERY = "yahooquery"
DATA_SOURCE_YAHOO_FINANCE = "yahoo_finance"

DATA_SOURCES = (
    (DATA_SOURCE_FINPREP, "Finprep"),
    (DATA_SOURCE_FINNHUB, "Finnhub"),
    (DATA_SOURCE_YFINANCE, "YFinance"),
    (DATA_SOURCE_YAHOOQUERY, "Yahooquery"),
    (DATA_SOURCE_YAHOO_FINANCE, "Yahoo Finance"),
)

DEFAULT_JSON_CHECKS_FILE = "src/empresas/company-checks.json"

MAX_REQUESTS_FINPREP = 250

STATEMENTS_TABLES = [
    "assets_companies_income_statements",
    "assets_companies_balance_sheet_statements",
    "assets_companies_cashflow_statements",
    "assets_companies_rentability_ratios",
    "assets_companies_liquidity_ratios",
    "assets_companies_margins_ratios",
    "assets_companies_freecashflow_ratios",
    "assets_companies_per_share_value",
    "assets_companies_non_gaap",
    "assets_companies_operations_risk_ratio",
    "assets_companies_enterprise_value_ratios",
    "assets_companies_growths",
    "assets_companies_eficiency_ratios",
    "assets_companies_price_to_ratios",
]

RATIOS_VALUES = [
    "rentability_ratios",
    "liquidity_ratios",
    "margins",
    "per_share_values",
    "operation_risks_ratios",
    "ev_ratios",
    "growth_rates",
    "price_to_ratios",
    "efficiency_ratios",
]

STATEMENTS = [
    "inc_statements",
    "balance_sheets",
    "cf_statements",
    "non_gaap_figures",
    "fcf_ratios",
] + RATIOS_VALUES
