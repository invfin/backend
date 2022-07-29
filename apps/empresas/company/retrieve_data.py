import random
import time
import requests

from datetime import datetime
from typing import Dict, List

import yahooquery as yq
import yfinance as yf

from django.conf import settings

FINHUB_TOKEN = settings.FINHUB_TOKEN
FINPREP_KEY = settings.FINPREP_KEY

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate'
}


class RetrieveCompanyData:
    def __init__(self, ticker) -> None:
        self.ticker = ticker
    
    def get_current_price(self):
        current_price = 0
        current_currency = 'None'

        try:
            company_info = yf.Ticker(self.ticker).info
            if 'currentPrice' in company_info:
                current_price = company_info['currentPrice']
                current_currency = company_info['currency']
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

    def scrap_price_yahoo(self):
        url_current_price = f'https://query1.finance.yahoo.com/v8/finance/chart/{self.ticker}'
        current_price_jsn = requests.get(url_current_price, headers=HEADERS).json()['chart']['result']
        current_price = [infos['meta']['regularMarketPrice'] for infos in current_price_jsn][0]
        current_currency = [infos['meta']['currency'] for infos in current_price_jsn][0]

        return current_price, current_currency
    
    def get_news(self):
        day = str(int(datetime.now().strftime("%Y-%m-%d")[-2:])-2)
        final_date = (datetime.now().strftime(f"%Y-%m-{day}"))
        return requests.get(f'https://finnhub.io/api/v1/company-news?symbol={self.ticker}&from={final_date}&to={datetime.now().strftime("%Y-%m-%d")}&token={FINHUB_TOKEN}').json()

    def request_income_statements_finprep(self) -> list:
        url_income_st = f'https://financialmodelingprep.com/api/v3/income-statement/{self.ticker}?limit=120&apikey={FINPREP_KEY}'
        inc_stt = requests.get(url_income_st,headers=HEADERS).json()
        return inc_stt

    def request_balance_sheets_finprep(self) -> list:
        url_balance_sheet = f'https://financialmodelingprep.com/api/v3/balance-sheet-statement/{self.ticker}?limit=120&apikey={FINPREP_KEY}'
        bal_sht = requests.get(url_balance_sheet,headers=HEADERS).json()
        return bal_sht

    def request_cashflow_statements_finprep(self) -> list:
        url_cashflow_st = f'https://financialmodelingprep.com/api/v3/cash-flow-statement/{self.ticker}?limit=120&apikey={FINPREP_KEY}'
        csf_stt = requests.get(url_cashflow_st,headers=HEADERS).json()
        return csf_stt
    
    def request_finprep(self) -> Dict[List, List]:
        random_int = random.randint(5,10)
        income_statements = self.request_income_statements_finprep()
        time.sleep(random_int)
        balance_sheets = self.request_balance_sheets_finprep()
        time.sleep(random_int)
        cashflow_statements = self.request_cashflow_statements_finprep()
        return {
            "income_statements": income_statements,
            "balance_sheets": balance_sheets,
            "cashflow_statements": cashflow_statements,
        }