


import yahooquery as yq
import yfinance as yf

from src.empresas.outils.valuations import discounted_cashflow
from src.general.utils import ChartSerializer


class CompanyExtended(ChartSerializer):
    currency_to_use = None



    def get_most_recent_price(self):
        yfinance_info = yf.Ticker(self.ticker).info
        if "currentPrice" in yfinance_info:
            current_price = yfinance_info["currentPrice"]
            current_currency = yfinance_info["currency"]
        else:
            yahooquery_info = yq.Ticker(self.ticker).price
            key = list(yahooquery_info.keys())[0]
            if yahooquery_info[key] != "Quote not found for ticker symbol: LB":
                current_price = yahooquery_info[key]["regularMarketPrice"]
                current_currency = yahooquery_info[key]["currency"]
            else:
                current_price = 0
                current_currency = ""
        return {"current_price": current_price, "current_currency": current_currency}
