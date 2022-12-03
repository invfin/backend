class ParseYahooFinance:
    def scrap_price_yahoo(self):
        url_current_price = f'https://query1.finance.yahoo.com/v8/finance/chart/{self.ticker}'
        current_price_jsn = requests.get(url_current_price, headers=HEADERS).json()['chart']['result']
        current_price = [infos['meta']['regularMarketPrice'] for infos in current_price_jsn][0]
        current_currency = [infos['meta']['currency'] for infos in current_price_jsn][0]

        return current_price, current_currency
