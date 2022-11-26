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

DEFAULT_JSON_CHECKS_FILE = "apps/empresas/company-checks.json"

MAX_REQUESTS_FINPREP = 120
