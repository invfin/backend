from datetime import datetime
from typing import Dict, List, Optional, Union

from django.db.models import QuerySet

from src.empresas.models import Company
from src.empresas.outils.financial_ratios.utils import (
    calculate_compound_growth,
    divide_or_zero,
)
from src.empresas.outils.valuations import discounted_cashflow, graham_value, margin_of_safety

from ..information_sources import FinnhubInfo, YahooQueryInfo, YFinanceInfo
from ..interfaces import AveragesInterface, CompanyInterface, StatementsInterface
from .chart_presentation import CompanyChartPresentation


class CompanyData:
    """
    Used to calcuate the current ratios and retreive the information in other places
    """

    company: CompanyInterface

    def __init__(self, company: Company, limit: int = 0):
        self.company = CompanyInterface(company)()
        self.limit = limit

    def show_all_information(self) -> Dict[str, Union[Dict[str, Union[int, float]], List]]:
        return CompanyChartPresentation().get_complete_information(self.get_statements())

    def get_statements(self) -> StatementsInterface:
        return self.company.load_statements()

    def get_averages(self) -> AveragesInterface:
        return self.company.load_averages()

    def get_ratios_information(self) -> dict:
        averages = self.get_averages().joint_averages()
        current_price = self.get_most_recent_price()
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
        current_eps = getattr(last_per_share, "eps", 0)
        marketcap = average_shares_out * current_price
        pfcf = divide_or_zero(current_price, getattr(last_per_share, "fcf_ps", 0))
        pb = divide_or_zero(current_price, getattr(last_per_share, "book_ps", 0))
        pta = divide_or_zero(current_price, getattr(last_per_share, "tangible_ps", 0))
        pcps = divide_or_zero(current_price, getattr(last_per_share, "cash_ps", 0))
        pocf = divide_or_zero(current_price, getattr(last_per_share, "operating_cf_ps", 0))
        per = divide_or_zero(current_price, current_eps)
        pas = divide_or_zero(current_price, getattr(last_per_share, "total_assets_ps", 0))
        peg = divide_or_zero(per, cagr).real
        ps = divide_or_zero(current_price, getattr(last_per_share, "sales_ps", 0))
        ev = (
            marketcap
            + getattr(last_balance_sheet, "total_debt", 0)
            - getattr(last_balance_sheet, "cash_and_short_term_investments", 0)
        )
        evebitda = divide_or_zero(ev, getattr(last_income_statement, "ebitda", 0))
        evsales = divide_or_zero(ev, last_revenue)
        gramvalu = graham_value(current_eps, getattr(last_per_share, "book_ps", 0))
        safety_margin_pes = margin_of_safety(gramvalu, current_price)
        fair_value = discounted_cashflow(
            last_revenue=last_revenue,
            revenue_growth=cagr,
            net_income_margin=getattr(last_margins, "net_income_margin", 0),
            fcf_margin=getattr(last_margins, "fcf_margin", 0),
            buyback=sharesbuyback,
            average_shares_out=average_shares_out,
        )
        safety_margin_opt = margin_of_safety(fair_value, current_price)
        most_used_ratios = CompanyChartPresentation().compare_most_used_ratios(
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
        averages |= {
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
        return averages

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

    def get_most_recent_price(self) -> int:
        return self.get_yahooquery_price() or self.get_yfinance_price() or 0

    def get_yfinance_price(self) -> Optional[int]:
        yfinance_info = YFinanceInfo(self.company.company).request_info_yfinance
        return yfinance_info.get("currentPrice")

    def get_yahooquery_price(self) -> Optional[int]:
        price = YahooQueryInfo(self.company.company).yahooquery.request_price_info_yahooquery
        return price.get("regularMarketPrice")

    def get_company_news(self) -> List[Dict[str, str]]:
        day = str(int(datetime.now().strftime("%Y-%m-%d")[-2:]) - 2)
        from_date = datetime.now().strftime(f"%Y-%m-{day}")
        to_date = datetime.now().strftime("%Y-%m-%d")
        return FinnhubInfo(self.company).company_news(
            self.company.company.ticker,
            from_date,
            to_date,
        )
