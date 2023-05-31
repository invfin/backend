from collections import defaultdict
from datetime import datetime
from typing import DefaultDict, Dict, Any

from django.db.models import Q

from ..information_sources import (
    FinnhubInfo,
    FinprepInfo,
    YahooQueryInfo,
    YFinanceInfo,
)
from src.empresas.outils.data_management.update.average_statements import AverageStatements
from src.empresas.outils.financial_ratios import CalculateFinancialRatios
from src.empresas.utils import log_company
from src.periods.constants import PERIOD_FOR_YEAR
from src.periods.models import Period
from src.translate.google_trans_new import google_translator


class UpdateCompany(CalculateFinancialRatios):
    def __init__(self, company) -> None:
        self.company = company

    @log_company()
    def add_logo(self) -> None:
        self.company.image = YFinanceInfo(self.company).request_info_yfinance["logo_url"]
        self.company.has_logo = True
        self.company.save(update_fields=["has_logo", "image"])
        return None

    @log_company()
    def add_description(self) -> None:
        self.company.description = google_translator().translate(
            self.company.description,
            lang_src="en",
            lang_tgt="es",
        )
        self.company.description_translated = True
        self.company.save(update_fields=["description_translated", "description"])
        return None

    def general_update(self) -> None:
        if not self.company.image:
            self.add_logo()
        if not self.company.description_translated:
            self.add_description()
        return None

    @log_company()
    def needs_update(self) -> bool:
        least_recent_date = YahooQueryInfo(
            self.company.ticker
        ).yahooquery.request_balance_sheets_yahooquery()
        least_recent_date = least_recent_date["asOfDate"].max().value // 10**9
        least_recent_year = datetime.fromtimestamp(least_recent_date).year
        return least_recent_year != self.company.most_recent_year

    @log_company()
    def update_average_financials_statements(self, period: Period) -> None:
        averager = AverageStatements(self.company)
        for funct_calculate_statement, funct_create_or_update_statement in [
            (
                averager.calculate_average_income_statement,
                self.create_or_update_inc_statements,
            ),
            (
                averager.calculate_average_balance_sheet,
                self.create_or_update_balance_sheets,
            ),
            (
                averager.calculate_average_cashflow_statement,
                self.create_or_update_cf_statements,
            ),
        ]:
            if averaged_stement := funct_calculate_statement(period):
                averaged_stement.update(**{"company": self.company, "from_average": True})
                funct_create_or_update_statement(averaged_stement, period)
        return None

    @log_company()
    def create_or_update_ttm(self) -> None:
        to_exclude = {
            "id",
            "period_id",
            "year",
            "company_id",
            "from_average",
            "is_ttm",
            "reported_currency_id",
        }
        for statement_manager in [
            self.company.inc_statements,
            self.company.balance_sheets,
            self.company.cf_statements,
        ]:
            result: DefaultDict = defaultdict(dict)
            for statement in statement_manager.filter(
                ~Q(period__period=PERIOD_FOR_YEAR),
                is_ttm=False,
            ).values()[:4]:
                for key, value in statement.items():
                    if key == "reported_currency_id":
                        result.setdefault(key, [])
                        result[key].append(value)
                    elif key == "date":
                        result[key] = max(result[key], value)
                    elif key not in to_exclude:
                        result[key] += value
            statement_manager.create(
                is_ttm=True,
                from_average=True,
                **AverageStatements.find_correct_currency(result),
                **result,
            )
        return None

    @log_company()
    def create_or_update_all_ratios(self, all_ratios: dict, period: Period) -> None:
        self.create_or_update_current_stock_price(
            price=all_ratios["current_price"],
        )
        self.create_or_update_rentability_ratios(
            all_ratios["rentability_ratios"],
            period=period,
        )
        self.create_or_update_liquidity_ratio(all_ratios["liquidity_ratio"], period=period)
        self.create_or_update_margin_ratio(all_ratios["margin_ratio"], period=period)
        self.create_or_update_fcf_ratio(all_ratios["fcf_ratio"], period=period)
        self.create_or_update_ps_value(all_ratios["ps_value"], period=period)
        self.create_or_update_non_gaap(all_ratios["non_gaap"], period=period)
        self.create_or_update_operation_risk_ratio(
            all_ratios["operation_risk_ratio"], period=period
        )
        self.create_or_update_price_to_ratio(all_ratios["price_to_ratio"], period=period)
        self.create_or_update_enterprise_value_ratio(
            all_ratios["enterprise_value_ratio"], period=period
        )
        self.create_or_update_efficiency_ratio(all_ratios["efficiency_ratio"], period=period)
        self.create_or_update_company_growth(all_ratios["company_growth"], period=period)
        return None

    @classmethod
    def create_or_update_statement(cls, data: dict, financial_model, period: Period) -> type:
        # Are these methods useless?
        statement, _ = financial_model.update_or_create(period=period, defaults=data)
        return statement

    @log_company()
    def create_or_update_inc_statements(self, data: dict, period: Period) -> type:
        return self.create_or_update_statement(data, self.company.inc_statements, period)

    @log_company()
    def create_or_update_balance_sheets(self, data: dict, period: Period) -> type:
        return self.create_or_update_statement(data, self.company.balance_sheets, period)

    @log_company()
    def create_or_update_cf_statements(self, data: dict, period: Period) -> type:
        return self.create_or_update_statement(data, self.company.cf_statements, period)

    @log_company()
    def create_or_update_current_stock_price(self, price):
        return self.company.stock_prices.create(price=price)

    @log_company()
    def create_or_update_rentability_ratios(self, data: dict, period: Period) -> type:
        return self.create_or_update_statement(data, self.company.rentability_ratios, period)

    @log_company()
    def create_or_update_liquidity_ratio(self, data: dict, period: Period) -> type:
        return self.create_or_update_statement(data, self.company.liquidity_ratios, period)

    @log_company()
    def create_or_update_margin_ratio(self, data: dict, period: Period) -> type:
        return self.create_or_update_statement(data, self.company.margins, period)

    @log_company()
    def create_or_update_fcf_ratio(self, data: dict, period: Period) -> type:
        return self.create_or_update_statement(data, self.company.fcf_ratios, period)

    @log_company()
    def create_or_update_ps_value(self, data: dict, period: Period) -> type:
        return self.create_or_update_statement(data, self.company.per_share_values, period)

    @log_company()
    def create_or_update_non_gaap(self, data: dict, period: Period) -> type:
        return self.create_or_update_statement(data, self.company.non_gaap_figures, period)

    @log_company()
    def create_or_update_operation_risk_ratio(self, data: dict, period: Period) -> type:
        return self.create_or_update_statement(
            data, self.company.operation_risks_ratios, period
        )

    @log_company()
    def create_or_update_enterprise_value_ratio(self, data: dict, period: Period) -> type:
        return self.create_or_update_statement(data, self.company.ev_ratios, period)

    @log_company()
    def create_or_update_company_growth(self, data: dict, period: Period) -> type:
        return self.create_or_update_statement(data, self.company.growth_rates, period)

    @log_company()
    def create_or_update_efficiency_ratio(self, data: dict, period: Period) -> type:
        return self.create_or_update_statement(data, self.company.efficiency_ratios, period)

    @log_company()
    def create_or_update_price_to_ratio(self, data: dict, period: Period) -> type:
        return self.create_or_update_statement(data, self.company.price_to_ratios, period)

    @log_company("latest_financials_finprep_info")
    def create_financials_finprep(self) -> Dict[str, Any]:
        return FinprepInfo(self.company).create_financials_finprep()

    @log_company("first_financials_finnhub_info")
    def create_financials_finnhub(self):
        return FinnhubInfo(self.company).create_financials_finnhub()

    @log_company("first_financials_yfinance_info")
    def create_financials_yfinance(self, period: str = "a"):
        if period == "q":
            return YFinanceInfo(self.company).create_quarterly_financials_yfinance()
        return YFinanceInfo(self.company).create_yearly_financials_yfinance()

    @log_company("first_financials_yahooquery_info")
    def create_financials_yahooquery(self, period: str = "a"):
        if period == "q":
            return YahooQueryInfo(self.company).create_quarterly_financials_yahooquery()
        return YahooQueryInfo(self.company).create_yearly_financials_yahooquery()

    @log_company("institutionals")
    def create_institutionals_yahooquery(self):
        return YahooQueryInfo(self.company).create_institutionals_yahooquery()

    @log_company("key_stats")
    def create_key_stats_yahooquery(self):
        return YahooQueryInfo(self.company).create_key_stats_yahooquery()
