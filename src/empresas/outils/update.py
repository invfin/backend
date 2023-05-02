from collections import defaultdict
from datetime import datetime

from django.db.models import Q

from src.empresas.parse.yahoo_query import ParseYahooQuery
from src.empresas.parse.y_finance import YFinanceInfo
from src.empresas.models import BalanceSheet, CashflowStatement, IncomeStatement
from src.empresas.outils.average_statements import AverageStatements
from src.empresas.outils.financial_ratios import CalculateFinancialRatios
from src.empresas.outils.retrieve_data import RetrieveCompanyData
from src.empresas.utils import FinprepRequestCheck, log_company
from src.periods.constants import PERIOD_FOR_YEAR
from src.periods.models import Period
from src.translate.google_trans_new import google_translator


class UpdateCompany(CalculateFinancialRatios):
    def __init__(self, company) -> None:
        self.company = company

    @log_company("fixed_last_finprep")
    def create_financials_finprep(self) -> None:
        if FinprepRequestCheck().manage_track_requests(3):
            finprep_data = RetrieveCompanyData(self.company).create_financials_finprep()
            income_statements = finprep_data["income_statements"]
            balance_sheets = finprep_data["balance_sheets"]
            cashflow_statements = finprep_data["cashflow_statements"]
            for income_statement in income_statements:
                IncomeStatement.objects.filter(
                    company=income_statement.company,
                    period=income_statement.period,
                ).update(**income_statement.return_standard())
            for balance_sheet in balance_sheets:
                BalanceSheet.objects.filter(
                    company=balance_sheet.company,
                    period=balance_sheet.period,
                ).update(**balance_sheet.return_standard())
            for cashflow_statement in cashflow_statements:
                CashflowStatement.objects.filter(
                    company=cashflow_statement.company,
                    period=cashflow_statement.period,
                ).update(**cashflow_statement.return_standard())
            # TODO add calculate ratios method
        return None

    @log_company()
    def add_logo(self) -> None:
        self.company.image = YFinanceInfo(self.company).request_info_yfinance["logo_url"]
        self.company.has_logo = True
        self.company.save(update_fields=["has_logo", "image"])
        return None

    @log_company()
    def add_description(self) -> None:
        self.company.description = google_translator().translate(
            self.company.description, lang_src="en", lang_tgt="es",
        )
        self.company.description_translated = True
        self.company.save(update_fields=["description_translated", "description"])
        return None

    def general_update(self) -> None:
        if not self.company.image:
            self.add_logo()
        if self.company.description_translated is False:
            self.add_description()
        return None

    @log_company()
    def check_last_filing(self) -> str:
        least_recent_date = ParseYahooQuery(self.company.ticker).balance_sheet()
        least_recent_date = least_recent_date["asOfDate"].max().value // 10**9
        least_recent_year = datetime.fromtimestamp(least_recent_date).year
        if least_recent_year != self.company.most_recent_year:
            return "need update"
        return "updated"

    @log_company()
    def update_average_financials_statements(self, period: Period) -> None:
        averager = AverageStatements(self.company)  # Inherit or like this?
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
                # Raise expect non arguments that why the type ignore
                averaged_stement.update({"company": self.company, "from_average": True})  # type: ignore
                funct_create_or_update_statement(averaged_stement, period)
        return None

    @log_company()
    def create_or_update_ttm(self) -> None:
        to_exclude = {"id",
                                "period_id",
                                "year",
                    "company_id",
              'from_average',
                    "is_ttm",
                    "reported_currency_id",}
        for statement_manager in [
            self.company.inc_statements,
            self.company.balance_sheets,
            self.company.cf_statements,
        ]:
            last_statements = statement_manager.filter(
                ~Q(period__period=PERIOD_FOR_YEAR), is_ttm=False,
            ).values()[:4]
            result = defaultdict(int)
            for statement in last_statements:
                for key, value in statement.items():
                    if key == "reported_currency_id":
                        result.setdefault(key, []) #type: ignore
                        result[key].append(value) #type: ignore
                    elif key == "date":
                        result[key] = max(result[key], value)
                    elif key not in to_exclude:
                        result[key] += value
            result.update(
                {
                    "is_ttm": True,
                    "from_average": True,
                    **AverageStatements.find_correct_currency(result)
                }
            )
            statement_manager.create(**result)
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
