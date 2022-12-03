from django.conf import settings

from src.empresas import constants
from src.general.outils.parser_client import ParserClient


class ParseFinnhub(ParserClient):
    base_path = constants.FINNHUB_BASE_URL
    api_version = constants.FINNHUB_API_VERSION
    auth = {"token": settings.FINNHUB_TOKEN}

    def company_profile(self, **dict_params):
        return self.request(path="stock", str_params="profile", dict_params=dict_params)

    def company_profile2(self, **dict_params):
        return self.request(path="stock", str_params="profile2", dict_params=dict_params)

    def aggregate_indicator(self, symbol, resolution):
        return self.request(
            path="scan",
            str_params="technical-indicator",
            dict_params={
                "symbol": symbol,
                "resolution": resolution,
            },
        )

    def crypto_exchanges(self):
        return self.request(path="crypto", str_params="exchange")

    def forex_exchanges(self):
        return self.request(path="forex", str_params="exchange")

    def press_releases(self, symbol, _from=None, to=None):
        return self.request(path="press-releases", dict_params={"symbol": symbol, "from": _from, "to": to})

    def company_executive(self, symbol):
        return self.request(path="stock", str_params="executive", dict_params={"symbol": symbol})

    def stock_dividends(self, symbol, _from=None, to=None):
        return self.request(
            path="stock", str_params="dividend", dict_params={"symbol": symbol, "from": _from, "to": to}
        )

    def stock_basic_dividends(self, symbol):
        return self.request(path="stock", str_params="dividend2", dict_params={"symbol": symbol})

    def stock_symbols(self, exchange, mic=None, security_type=None, currency=None):
        return self.request(
            path="stock",
            str_params="symbol",
            dict_params={"exchange": exchange, "mic": mic, "securityType": security_type, "currency": currency},
        )

    def recommendation_trends(self, symbol):
        return self.request(path="stock", str_params="recommendation", dict_params={"symbol": symbol})

    def price_target(self, symbol):
        return self.request(path="stock", str_params="price-target", dict_params={"symbol": symbol})

    def upgrade_downgrade(self, symbol=None, _from=None, to=None):
        return self.request(
            path="stock", str_params="upgrade-downgrade", dict_params={"symbol": symbol, "from": _from, "to": to}
        )

    def option_chain(self, **dict_params):
        return self.request(path="stock", str_params="option-chain", dict_params=dict_params)

    def company_peers(self, symbol):
        return self.request(path="stock", str_params="peers", dict_params={"symbol": symbol})

    def company_basic_financials(self, symbol, metric):
        return self.request(path="stock", str_params="metric", dict_params={"symbol": symbol, "metric": metric})

    def financials(self, symbol, statement, freq):
        return self.request(
            path="stock", str_params="financials", dict_params={"symbol": symbol, "statement": statement, "freq": freq}
        )

    def financials_reported(self, **dict_params):
        return self.request(path="stock", str_params="financials-reported", dict_params=dict_params)

    def fund_ownership(self, symbol, limit=None):
        return self.request(path="stock", str_params="fund-ownership", dict_params={"symbol": symbol, "limit": limit})

    def company_earnings(self, symbol, limit=None):
        return self.request(path="stock", str_params="earnings", dict_params={"symbol": symbol, "limit": limit})

    def company_revenue_estimates(self, symbol, freq=None):
        return self.request(path="stock", str_params="revenue-estimate", dict_params={"symbol": symbol, "freq": freq})

    def company_ebitda_estimates(self, symbol, freq=None):
        return self.request(path="stock", str_params="ebitda-estimate", dict_params={"symbol": symbol, "freq": freq})

    def company_ebit_estimates(self, symbol, freq=None):
        return self.request(path="stock", str_params="ebit-estimate", dict_params={"symbol": symbol, "freq": freq})

    def company_eps_estimates(self, symbol, freq=None):
        return self.request(path="stock", str_params="eps-estimate", dict_params={"symbol": symbol, "freq": freq})

    def exchange(self):
        return self.request(path="stock", str_params="exchange")

    def filings(self, **dict_params):
        return self.request(path="stock", str_params="filings", dict_params=dict_params)

    def stock_symbol(self, **dict_params):
        return self.request(path="stock", str_params="symbol", dict_params=dict_params)

    def quote(self, symbol):
        return self.request(path="quote", dict_params={"symbol": symbol})

    def transcripts(self, _id):
        return self.request(path="stock", str_params="transcripts", dict_params={"id": _id})

    def transcripts_list(self, symbol):
        return self.request(path="stock", str_params="transcripts/list", dict_params={"symbol": symbol})

    def sim_index(self, **dict_params):
        return self.request(path="stock", str_params="similarity-index", dict_params=dict_params)

    # def stock_candles(self, symbol, resolution, _from, to, **kwargs):
    #     dict_params = self._merge_two_dicts({
    #         "symbol": symbol,
    #         "resolution": resolution,
    #         "from": _from,
    #         "to": to
    #     }, kwargs)
    #
    #     return self.request(path="stock", str_params="candle", dict_params=dict_params)
    #
    # def stock_tick(self, symbol, date, limit, skip, _format='json', **kwargs):
    #     dict_params = self._merge_two_dicts({
    #         "symbol": symbol,
    #         "date": date,
    #         "limit": limit,
    #         "skip": skip,
    #         "format": _format
    #     }, kwargs)
    #
    #     return self.request(path="stock", str_params="tick", dict_params=dict_params)

    # def stock_nbbo(self, symbol, date, limit, skip, _format='json', **kwargs):
    #     dict_params = self._merge_two_dicts({
    #         "symbol": symbol,
    #         "date": date,
    #         "limit": limit,
    #         "skip": skip,
    #         "format": _format
    #     }, kwargs)

    # return self.request(path="stock", str_params="bbo", dict_params=dict_params)

    def forex_rates(self, **dict_params):
        return self.request(path="forex", str_params="rates", dict_params=dict_params)

    def forex_symbols(self, exchange):
        return self.request(path="forex", str_params="symbol", dict_params={"exchange": exchange})

    def forex_candles(self, symbol, resolution, _from, to, _format="json"):
        return self.request(
            path="forex",
            str_params="candle",
            dict_params={"symbol": symbol, "resolution": resolution, "from": _from, "to": to, "format": _format},
        )

    def crypto_symbols(self, exchange):
        return self.request(path="crypto", str_params="symbol", dict_params={"exchange": exchange})

    def crypto_candles(self, symbol, resolution, _from, to, _format="json"):
        return self.request(
            path="crypto",
            str_params="candle",
            dict_params={"symbol": symbol, "resolution": resolution, "from": _from, "to": to, "format": _format},
        )

    def pattern_recognition(self, symbol, resolution):
        return self.request(path="scan", str_params="pattern", dict_params={"symbol": symbol, "resolution": resolution})

    def support_resistance(self, symbol, resolution):
        return self.request(
            path="scan", str_params="support-resistance", dict_params={"symbol": symbol, "resolution": resolution}
        )

    # def technical_indicator(self, symbol, resolution, _from, to, indicator, indicator_fields=None):
    #     indicator_fields = indicator_fields or {}
    #     dict_params = self._merge_two_dicts({
    #         "symbol": symbol,
    #         "resolution": resolution,
    #         "from": _from,
    #         "to": to,
    #         "indicator": indicator
    #     }, indicator_fields)
    #
    #     return self.request(path="indicator", dict_params=dict_params)

    def stock_splits(self, symbol, _from, to):
        return self.request(path="stock", str_params="split", dict_params={"symbol": symbol, "from": _from, "to": to})

    def general_news(self, category, min_id=0):
        return self.request(path="news", dict_params={"category": category, "minId": min_id})

    def company_news(self, symbol, _from, to):
        return self.request(path="company-news", dict_params={"symbol": symbol, "from": _from, "to": to})

    def news_sentiment(self, symbol):
        return self.request(path="news-sentiment", dict_params={"symbol": symbol})

    def ownership(self, symbol, limit=None):
        return self.request(path="stock", str_params="ownership", dict_params={"symbol": symbol, "limit": limit})

    def country(self):
        return self.request(path="country")

    def economic_code(self):
        return self.request(path="economic", str_params="code")

    def economic_data(self, code):
        return self.request(path="economic", dict_params={"code": code})

    def calendar_economic(self, _from=None, to=None):
        return self.request(path="calendar", str_params="economic", dict_params={"from": _from, "to": to})

    def earnings_calendar(self, _from, to, symbol, international=False):
        return self.request(
            path="calendar",
            str_params="earnings",
            dict_params={"from": _from, "to": to, "symbol": symbol, "international": international},
        )

    def ipo_calendar(self, _from, to):
        return self.request(path="calendar", str_params="ipo", dict_params={"from": _from, "to": to})

    def indices_const(self, **dict_params):
        return self.request(path="index", str_params="constituents", dict_params=dict_params)

    def indices_hist_const(self, **dict_params):
        return self.request(path="index", str_params="historical-constituents", dict_params=dict_params)

    def etfs_profile(self, symbol=None, isin=None):
        return self.request(path="etf", str_params="profile", dict_params={"symbol": symbol, "isin": isin})

    def etfs_holdings(self, symbol=None, isin=None, skip=None, date=None):
        return self.request(
            path="etf", str_params="holdings", dict_params={"symbol": symbol, "isin": isin, "skip": skip, "date": date}
        )

    def etfs_sector_exp(self, symbol):
        return self.request(path="etf", str_params="sector", dict_params={"symbol": symbol})

    def etfs_country_exp(self, symbol):
        return self.request(path="etf", str_params="country", dict_params={"symbol": symbol})

    def international_filings(self, symbol="", country=""):
        return self.request(
            path="stock", str_params="international-filings", dict_params={"symbol": symbol, "country": country}
        )

    def sec_sentiment_analysis(self, access_number):
        return self.request(path="stock", str_params="filings-sentiment", dict_params={"accessNumber": access_number})

    def sec_similarity_index(self, symbol="", cik="", freq="annual"):
        return self.request(
            path="stock", str_params="similarity-index", dict_params={"symbol": symbol, "cik": cik, "freq": freq}
        )

    def last_bid_ask(self, symbol):
        return self.request(path="stock", str_params="bidask", dict_params={"symbol": symbol})

    def fda_calendar(self):
        return self.request("fda-advisory-committee-calendar")

    def symbol_lookup(self, query):
        return self.request("search", dict_params={"q": query})

    def stock_insider_transactions(self, symbol, _from=None, to=None):
        return self.request(
            path="stock", str_params="insider-transactions", dict_params={"symbol": symbol, "from": _from, "to": to}
        )

    def mutual_fund_profile(self, symbol=None, isin=None):
        return self.request(path="mutual-fund", str_params="profile", dict_params={"symbol": symbol, "isin": isin})

    def mutual_fund_holdings(self, symbol=None, isin=None, skip=None):
        return self.request(
            path="mutual-fund", str_params="holdings", dict_params={"symbol": symbol, "isin": isin, "skip": skip}
        )

    def mutual_fund_sector_exp(self, symbol):
        return self.request(path="mutual-fund", str_params="sector", dict_params={"symbol": symbol})

    def mutual_fund_country_exp(self, symbol):
        return self.request(path="mutual-fund", str_params="country", dict_params={"symbol": symbol})

    def stock_revenue_breakdown(self, symbol, cik=""):
        return self.request(path="stock", str_params="revenue-breakdown", dict_params={"symbol": symbol, "cik": cik})

    def stock_social_sentiment(self, symbol, _from=None, to=None):
        return self.request(
            path="stock", str_params="social-sentiment", dict_params={"symbol": symbol, "from": _from, "to": to}
        )

    def stock_investment_theme(self, theme):
        return self.request(path="stock", str_params="investment-theme", dict_params={"theme": theme})

    def stock_supply_chain(self, symbol):
        return self.request(path="stock", str_params="supply-chain", dict_params={"symbol": symbol})

    def company_esg_score(self, symbol):
        return self.request(path="stock", str_params="esg", dict_params={"symbol": symbol})

    def company_earnings_quality_score(self, symbol, freq):
        return self.request(
            path="stock", str_params="earnings-quality-score", dict_params={"symbol": symbol, "freq": freq}
        )

    def crypto_profile(self, symbol):
        return self.request(path="crypto", str_params="profile", dict_params={"symbol": symbol})

    def stock_uspto_patent(self, symbol, _from=None, to=None):
        return self.request(
            path="stock", str_params="uspto-patent", dict_params={"symbol": symbol, "from": _from, "to": to}
        )

    def stock_visa_application(self, symbol, _from=None, to=None):
        return self.request(
            path="stock", str_params="visa-application", dict_params={"symbol": symbol, "from": _from, "to": to}
        )

    def stock_insider_sentiment(self, symbol, _from, to):
        return self.request(
            path="stock", str_params="insider-sentiment", dict_params={"symbol": symbol, "from": _from, "to": to}
        )

    def stock_lobbying(self, symbol, _from, to):
        return self.request(
            path="stock", str_params="lobbying", dict_params={"symbol": symbol, "from": _from, "to": to}
        )

    def bond_profile(self, **dict_params):
        return self.request(path="bond", str_params="profile", dict_params=dict_params)

    def bond_price(self, isin, _from, to):
        return self.request(path="bond", str_params="price", dict_params={"isin": isin, "from": _from, "to": to})

    def stock_usa_spending(self, symbol, _from, to):
        return self.request(
            path="stock", str_params="usa-spending", dict_params={"symbol": symbol, "from": _from, "to": to}
        )

    # def get_news(self, symbol):
    #     day = str(int(datetime.now().strftime("%Y-%m-%d")[-2:])-2)
    #     final_date = (datetime.now().strftime(f"%Y-%m-{day}"))
    #     return requests.get(f'https://finnhub.io/api/v1/company-news?symbol={symbol}&from={final_date}&to={datetime.now().strftime("%Y-%m-%d")}&token={FINNHUB_TOKEN}').json()
