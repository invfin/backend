from typing import Any, Dict, List, Union

from django.db.models import QuerySet

from src.empresas.models import Company
from src.empresas.querysets.statements import StatementQuerySet

from src.empresas.outils.financial_ratios.utils import (
    calculate_compound_growth,
    divide_or_zero,
)
from src.empresas.outils.valuations import discounted_cashflow, graham_value, margin_of_safety
from ..interfaces import CompanyInterface, StatementsInterface, AveragesInterface
from ..information_sources import (
    FinnhubInfo,
    FinprepInfo,
    YahooQueryInfo,
    YFinanceInfo,
)


class CompanyData:
    """
    Used to calcuate the current ratios and retreive the information in other places
    """

    company: Company

    def __init__(self, company: Company, limit: int = 0):
        self.company = company
        self.limit = limit

    def get_ratios_information(self):
        return self.get_current_ratios(self.get_averages(self.get_statements()))

    def get_statements(
        self,
    ) -> Dict[str, Union[StatementQuerySet, Dict[str, Union[int, float]]]]:
        # TODO add a prefetch to get all at once
        return {
            "inc_statements": self.company.inc_statements.yearly_exclude_ttm(),  # type: ignore
            "balance_sheets": self.company.balance_sheets.yearly_exclude_ttm(),  # type: ignore
            "cf_statements": self.company.cf_statements.yearly_exclude_ttm(),  # type: ignore
            "rentability_ratios": self.company.rentability_ratios.yearly_exclude_ttm(),  # type: ignore
            "liquidity_ratios": self.company.liquidity_ratios.yearly_exclude_ttm(),  # type: ignore
            "margins": self.company.margins.yearly_exclude_ttm(),  # type: ignore
            "fcf_ratios": self.company.fcf_ratios.yearly_exclude_ttm(),  # type: ignore
            "per_share_values": self.company.per_share_values.yearly_exclude_ttm(),  # type: ignore
            "non_gaap_figures": self.company.non_gaap_figures.yearly_exclude_ttm(),  # type: ignore
            "operation_risks_ratios": self.company.operation_risks_ratios.yearly_exclude_ttm(),  # type: ignore
            "ev_ratios": self.company.ev_ratios.yearly_exclude_ttm(),  # type: ignore
            "growth_rates": self.company.growth_rates.yearly_exclude_ttm(),  # type: ignore
            "efficiency_ratios": self.company.efficiency_ratios.yearly_exclude_ttm(),  # type: ignore
            "price_to_ratios": self.company.price_to_ratios.yearly_exclude_ttm(),  # type: ignore
        }

    @staticmethod
    def get_averages(
        statements: Dict[str, Union[StatementQuerySet, Dict[str, Union[int, float]]]],
    ) -> Dict[str, Union[StatementQuerySet, Dict[str, Union[int, float]]]]:
        statements["averages"] = {
            **statements["rentability_ratios"].average_rentability_ratios(),
            **statements["liquidity_ratios"].average_liquidity_ratios(),
            **statements["margins"].average_margins(),
            **statements["per_share_values"].average_per_share_values(),
            **statements["operation_risks_ratios"].average_operation_risks_ratios(),
            **statements["ev_ratios"].average_ev_ratios(),
            **statements["growth_rates"].average_growth_rates(),
            **statements["price_to_ratios"].average_price_to_ratios(),
            **statements["efficiency_ratios"].average_efficiency_ratios(),
        }
        return statements  # type: ignore

    def get_current_ratios(
        self,
        statements: Dict[str, QuerySet],
    ) -> dict:
        # TODO test
        averages = statements.pop("averages")
        current_price = self.get_most_recent_price(self.company.ticker)["current_price"]
        last_balance_sheet = statements["balance_sheets"].first()
        last_per_share = statements["per_share_values"].first()
        last_margins = statements["margins"].first()
        all_inc_statements = statements["inc_statements"]
        last_income_statement = all_inc_statements.first()
        last_revenue = last_income_statement.revenue or 0
        average_shares_out = last_income_statement.weighted_average_shares_outstanding or 0
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
        if not self.company.currency:
            try:
                currency = statement[0].reported_currency
            except Exception:
                currency = None
            else:
                self.company.currency = currency
                self.company.save(update_fields=["currency"])
        else:
            currency = self.company.currency
        return currency.currency if currency else "$"

    @classmethod
    def get_most_recent_price(cls, ticker) -> Dict[str, Union[int, str]]:
        price, currency = cls.get_yfinance_price(ticker)
        if not price:
            price, currency = cls.get_yahooquery_price(ticker)
        price = price or 0
        currency = currency or ""
        return {"current_price": price, "current_currency": currency}

    @staticmethod
    def get_yfinance_price(ticker):
        yfinance_info = yf.Ticker(ticker).info
        current_price = yfinance_info.get("currentPrice")
        current_currency = yfinance_info.get("currency")
        return current_price, current_currency

    @staticmethod
    def get_yahooquery_price(ticker):
        yahooquery_info = yq.Ticker(ticker).price.get(ticker, {})
        if yahooquery_info == f"Quote not found for ticker symbol: {ticker}":
            yahooquery_info = {}
        current_price = yahooquery_info.get("regularMarketPrice")
        current_currency = yahooquery_info.get("currency")
        return current_price, current_currency

    def get_company_news(self) -> List[Dict[str, str]]:
        day = str(int(datetime.now().strftime("%Y-%m-%d")[-2:]) - 2)
        from_date = datetime.now().strftime(f"%Y-%m-{day}")
        to_date = datetime.now().strftime("%Y-%m-%d")
        return FinnhubInfo(self.company).company_news(self.company.ticker, from_date, to_date)
