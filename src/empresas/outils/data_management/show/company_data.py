from datetime import datetime
from typing import Dict, List, Union

from django.db.models import QuerySet

from src.empresas.models import Company
from src.empresas.outils.financial_ratios.utils import (
    calculate_compound_growth,
    divide_or_zero,
)
from src.empresas.outils.valuations import discounted_cashflow, graham_value, margin_of_safety

from ..interfaces import CompanyInterface, StatementsInterface, AveragesInterface
from ..information_sources import (
    FinnhubInfo,
    YahooQueryInfo,
    YFinanceInfo,
)


class CompanyData:
    """
    Used to calcuate the current ratios and retreive the information in other places
    """

    company: CompanyInterface

    def __init__(self, company: Company, limit: int = 0):
        self.company = CompanyInterface(company)()
        self.limit = limit

    def get_statements(self) -> StatementsInterface:
        return self.company.load_statements()

    def get_averages(self) -> AveragesInterface:
        return self.company.load_averages()

    def get_ratios_information(self) -> dict:
        current_price = self.get_most_recent_price()["current_price"]
        last_balance_sheet = self.company.statements.balance_sheets.first()
        last_per_share = self.company.statements.per_share_values.first()
        last_margins = self.company.statements.margins.first()
        all_inc_statements = self.company.statements.inc_statements
        last_income_statement = all_inc_statements.first()
        last_revenue = getattr(last_income_statement, "revenue", 0)
        average_shares_out = getattr(
            last_income_statement,
            "weighted_average_shares_outstanding",
            0,
        )
        num_ics = min(all_inc_statements.count(), 10)
        number = num_ics - 1
        sharesbuyback = abs(
            calculate_compound_growth(
                average_shares_out,
                all_inc_statements[number].weighted_average_shares_outstanding,
                num_ics,
            )
        )
        cagr = calculate_compound_growth(
            last_revenue, all_inc_statements[number].revenue, num_ics
        )
        current_eps = last_per_share.eps or 0
        marketcap = average_shares_out * current_price
        pfcf = divide_or_zero(current_price, last_per_share.fcf_ps or 0)
        pb = divide_or_zero(current_price, last_per_share.book_ps or 0)
        pta = divide_or_zero(current_price, last_per_share.tangible_ps or 0)
        pcps = divide_or_zero(current_price, last_per_share.cash_ps or 0)
        pocf = divide_or_zero(current_price, last_per_share.operating_cf_ps or 0)
        per = divide_or_zero(current_price, current_eps)
        pas = divide_or_zero(current_price, last_per_share.total_assets_ps or 0)
        peg = divide_or_zero(per, cagr).real
        ps = divide_or_zero(current_price, last_per_share.sales_ps or 0)
        ev = (
            marketcap + last_balance_sheet.total_debt
            or 0 - last_balance_sheet.cash_and_short_term_investments
            or 0
        )
        evebitda = divide_or_zero(ev, last_income_statement.ebitda or 0)
        evsales = divide_or_zero(ev, last_revenue)
        gramvalu = graham_value(current_eps, last_per_share.book_ps or 0)
        safety_margin_pes = margin_of_safety(gramvalu, current_price)
        fair_value = discounted_cashflow(
            last_revenue=last_revenue,
            revenue_growth=cagr,
            net_income_margin=last_margins.net_income_margin or 0,
            fcf_margin=last_margins.fcf_margin or 0,
            buyback=sharesbuyback,
            average_shares_out=average_shares_out,
        )
        safety_margin_opt = margin_of_safety(fair_value, current_price)
        most_used_ratios = self.compare_most_used_ratios(
            per,
            pb,
            ps,
            pfcf,
            peg,
            pas,
            pcps,
            pta,
            pocf,
            evebitda,
            evsales,
            averages,
        )
        averages.update(
            {
                "most_used_ratios": most_used_ratios,
                "pfcf": pfcf,
                "pas": pas,
                "pta": pta,
                "pcps": pcps,
                "pocf": pocf,
                "per": per,
                "pb": pb,
                "peg": peg,
                "ps": ps,
                "fair_value": fair_value,
                "ev": ev,
                "marketcap": marketcap,
                "cagr": cagr,
                "evebitda": evebitda,
                "evsales": evsales,
                "gramvalu": gramvalu,
                "sharesbuyback": sharesbuyback,
                "safety_margin_pes": safety_margin_pes,
                "safety_margin_opt": safety_margin_opt,
                "current_price": current_price,
                "last_revenue": last_revenue,
                "average_shares_out": average_shares_out,
                "last_balance_sheet": last_balance_sheet,
                "last_per_share": last_per_share,
                "last_margins": last_margins,
                "last_income_statement": last_income_statement,
            }
        )
        return averages

    def calculate_most_used_ratios(self):
        pass

    def get_currency(self, statement: QuerySet) -> str:
        if not self.company.company.currency:
            try:
                currency = statement[0].reported_currency
            except Exception:
                currency = None
            else:
                self.company.company.currency = currency
                self.company.company.save(update_fields=["currency"])
        else:
            currency = self.company.company.currency
        return currency.currency if currency else "$"

    def get_most_recent_price(self) -> Dict[str, Union[int, str]]:
        price, currency = self.get_yfinance_price()
        if not price:
            price, currency = self.get_yahooquery_price()
        price = price or 0
        currency = currency or ""
        return {"current_price": price, "current_currency": currency}

    def get_yfinance_price(self):
        yfinance_info = YFinanceInfo(self.company.company).request_info_yfinance
        current_price = yfinance_info.get("currentPrice")
        current_currency = yfinance_info.get("currency")
        return current_price, current_currency

    def get_yahooquery_price(self):
        price = YahooQueryInfo(self.company.company).yahooquery.request_price_info_yahooquery
        current_price = price.get("regularMarketPrice")
        current_currency = price.get("currency")
        return current_price, current_currency

    def get_company_news(self) -> List[Dict[str, str]]:
        day = str(int(datetime.now().strftime("%Y-%m-%d")[-2:]) - 2)
        from_date = datetime.now().strftime(f"%Y-%m-{day}")
        to_date = datetime.now().strftime("%Y-%m-%d")
        return FinnhubInfo(self.company).company_news(
            self.company.company.ticker, from_date, to_date
        )
