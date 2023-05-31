import yahooquery as yq

from .exceptions import TickerNotFound


class ParseYahooQuery:
    ticker: str

    def __init__(self, ticker: str) -> None:
        self.ticker = ticker

    @property
    def yqcompany(self):
        return yq.Ticker(self.ticker)

    @property
    def request_price_info_yahooquery(self):
        if self.yqcompany.price == {self.ticker: f"Quote not found for ticker symbol: {self.ticker}"}:
            raise TickerNotFound(self.ticker)
        return self.yqcompany.price

    @property
    def request_earning_history_yahooquery(self):
        return self.yqcompany.earning_history

    @property
    def request_key_stats_yahooquery(self):
        return self.yqcompany.key_stats

    def request_income_statements_yahooquery(self, frequency: str = "a", trailing=False):
        return self.yqcompany.income_statement(frequency=frequency, trailing=trailing)

    def request_balance_sheets_yahooquery(self, frequency: str = "a", trailing=False):
        return self.yqcompany.balance_sheet(frequency=frequency, trailing=trailing)

    def request_cashflow_statements_yahooquery(self, frequency: str = "a", trailing=False):
        return self.yqcompany.cash_flow(frequency=frequency, trailing=trailing)
