import yahooquery as yq

from src.empresas.outils.data_management.information_sources.y_finance import YFinanceInfo


def simple_stock_analysis(empresa):
    inf = YFinanceInfo(empresa).request_info_yfinance
    current_price = inf.get("currentPrice")
    result = {"result": 4}
    if not current_price:
        yahooquery_info = yq.Ticker(empresa.ticker).price
        key = yahooquery_info.keys()[0]  # type: ignore
        if yahooquery_info[key] != "Quote not found for ticker symbol: LB":
            current_price = yahooquery_info[key]["regularMarketPrice"]  # type: ignore

    result_buy = {"result": 1}

    result_sell = {"result": 2}

    result_hold = {"result": 3}

    if "recommendationKey" in inf:
        recommendationKey = inf["recommendationKey"]
        if recommendationKey == "buy":
            result = result_buy
        elif recommendationKey == "hold":
            result = result_hold
        elif recommendationKey == "sell":
            result = result_sell

    else:
        if "targetMeanPrice" in inf:
            targetMeanPrice = inf["targetMeanPrice"]
            if targetMeanPrice < current_price:
                result = result_sell
            elif targetMeanPrice > current_price:
                result = result_buy
            elif targetMeanPrice == current_price:
                result = result_hold

        else:
            current_price = inf["currentPrice"]
            try:
                per = empresa.per_share_values.latest().eps / current_price
                if per < 10:
                    result = result_buy
                elif per > 20:
                    result = result_sell
                elif per > 10 and per < 20:
                    result = result_hold
            except Exception:
                pass

    return result
