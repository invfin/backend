import yahooquery as yq


class ParseYahooQuery:
    def institutional_ownership(self):
        df = self.yq_company.institution_ownership
        df = df.reset_index()
        df = df.drop(columns=['symbol', 'row', 'maxAge'])
        try:
            log_message = 'all right'
            for index, data in df.iterrows():
                pass
        except:
            pass

    def get_current_price(self):
        current_price = 0
        current_currency = 'None'

        try:
            else:
                company_info = yq.Ticker(self.ticker).financial_data
                if 'currentPrice' in company_info:
                    current_price = company_info['currentPrice']
                    current_currency = company_info['financialCurrency']

        except Exception as e:
            current_price, current_currency = self.scrap_price_yahoo()

        return {
            'current_price': current_price,
            'current_currency': current_currency,
        }
