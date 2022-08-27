import yahooquery as yq


class ParseYahooQuery:
    company = None

    @property
    def yqcompany(self):
        return yq.Ticker(self.company.ticker)

    @property
    def request_price_info_yahooquery(self):
        return self.yqcompany.price

    @property
    def request_key_stats_yahooquery(self):
        return self.yqcompany.key_stats

    def request_income_statements_yahooquery(self, frequency: str = "a", trailing=False):
        return self.yqcompany.income_statement(frequency=frequency, trailing=trailing)

    def request_balance_sheets_yahooquery(self, frequency: str = "a", trailing=False):
        return self.yqcompany.balance_sheet(frequency=frequency, trailing=trailing)

    def request_cashflow_statements_yahooquery(self, frequency: str = "a", trailing=False):
        return self.yqcompany.cash_flow(frequency=frequency, trailing=trailing)

    # def get_current_price(self):
    #     current_price = 0
    #     current_currency = 'None'

    #     try:
    #         else:
    #             company_info = yq.Ticker(self.ticker).financial_data
    #             if 'currentPrice' in company_info:
    #                 current_price = company_info['currentPrice']
    #                 current_currency = company_info['financialCurrency']

    #     except Exception as e:
    #         current_price, current_currency = self.scrap_price_yahoo()

    #     return {
    #         'current_price': current_price,
    #         'current_currency': current_currency,
    #     }
