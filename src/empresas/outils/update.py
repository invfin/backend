from datetime import datetime

from django.db.models import Q

from src.empresas.models import BalanceSheet, CashflowStatement, IncomeStatement
from src.empresas.outils.average_statements import AverageStatements
from src.empresas.outils.financial_ratios import CalculateFinancialRatios
from src.empresas.outils.retrieve_data import RetrieveCompanyData
from src.empresas.utils import FinprepRequestCheck, log_company
from src.periods.constants import PERIOD_FOR_YEAR
from src.translate.google_trans_new import google_translator


class UpdateCompany(CalculateFinancialRatios, AverageStatements):
    def __init__(self, company) -> None:
        self.company = company

    @log_company("fixed_last_finprep")
    def create_financials_finprep(self) -> None:
        if FinprepRequestCheck().manage_track_requests(3):
            finprep_data = RetrieveCompanyData(self.company).finprep.create_financials_finprep()
            income_statements = finprep_data["income_statements"]
            balance_sheets = finprep_data["balance_sheets"]
            cashflow_statements = finprep_data["cashflow_statements"]
            for income_statement in income_statements:
                IncomeStatement.objects.filter(
                    company=income_statement.company,
                    period=income_statement.period,
                ).update(**income_statement.return_standard)
            for balance_sheet in balance_sheets:
                BalanceSheet.objects.filter(
                    company=balance_sheet.company,
                    period=balance_sheet.period,
                ).update(**balance_sheet.return_standard)
            for cashflow_statement in cashflow_statements:
                CashflowStatement.objects.filter(
                    company=cashflow_statement.company,
                    period=cashflow_statement.period,
                ).update(**cashflow_statement.return_standard)
            # TODO add calculate ratios method
        return None

    @log_company()
    def add_logo(self):
        self.company.image = self.request_info_yfinance["logo_url"]
        self.company.has_logo = True
        self.company.save(update_fields=["has_logo", "image"])

    @log_company()
    def add_description(self):
        self.company.description = google_translator().translate(self.company.description, lang_src="en", lang_tgt="es")
        self.company.description_translated = True
        self.company.save(update_fields=["description_translated", "description"])

    def general_update(self):
        if not self.company.image:
            self.add_logo()
        if self.company.description_translated is False:
            self.add_description()

    @log_company()
    def check_last_filing(self):
        least_recent_date = self.yq_company.balance_sheet()
        least_recent_date = least_recent_date["asOfDate"].max().value // 10**9  # normalize time
        least_recent_year = datetime.fromtimestamp(least_recent_date).year
        if least_recent_year != self.company.most_recent_year:
            return "need update"
        return "updated"

    @log_company()
    def update_average_financials_statements(self, period):
        """
        TODO
        Move all the calculation logic into SQL
        """
        for funct_calculate_statement, funct_create_or_update_statement in [
            (self.calculate_average_income_statement, self.create_or_update_inc_statements),
            (self.calculate_average_balance_sheet, self.create_or_update_balance_sheets),
            (self.calculate_average_cashflow_statement, self.create_or_update_cf_statements),
        ]:
            averaged_stement = funct_calculate_statement(period)
            if averaged_stement:
                averaged_stement.update({"company": self.company, "from_average": True})
                funct_create_or_update_statement(averaged_stement, period)

    @log_company()
    def create_or_update_ttm(self):
        for statement_manager in [
            self.company.inc_statements,
            self.company.balance_sheets,
            self.company.cf_statements,
        ]:
            last_statements = statement_manager.filter(~Q(period__period=PERIOD_FOR_YEAR), is_ttm=False)[:4]
            ttm_dict = {}
            for statement in last_statements:
                st_dict = statement.__dict__
                for field in ["_state", "id", "period_id", "year", "company_id", "is_ttm", "reported_currency_id"]:
                    st_dict.pop(field)
                date = st_dict.pop("date")
                if "date" not in ttm_dict:
                    ttm_dict["date"] = date
                for key, value in st_dict.items():
                    if key in ttm_dict:
                        ttm_dict[key] += value
                    else:
                        ttm_dict[key] = value
            ttm_dict.update(
                {
                    "is_ttm": True,
                    "from_average": True,
                }
            )
            statement_manager.create(**ttm_dict)

    @log_company()
    def create_or_update_all_ratios(self, all_ratios: dict) -> None:
        self.create_or_update_current_stock_price(price=all_ratios["current_data"]["currentPrice"])
        self.create_or_update_rentability_ratios(all_ratios["rentability_ratios"])
        self.create_or_update_liquidity_ratio(all_ratios["liquidity_ratio"])
        self.create_or_update_margin_ratio(all_ratios["margin_ratio"])
        self.create_or_update_fcf_ratio(all_ratios["fcf_ratio"])
        self.create_or_update_ps_value(all_ratios["ps_value"])
        self.create_or_update_non_gaap(all_ratios["non_gaap"])
        self.create_or_update_operation_risk_ratio(all_ratios["operation_risk_ratio"])
        self.create_or_update_price_to_ratio(all_ratios["price_to_ratio"])
        self.create_or_update_enterprise_value_ratio(all_ratios["enterprise_value_ratio"])
        self.create_or_update_efficiency_ratio(all_ratios["efficiency_ratio"])
        self.create_or_update_company_growth(all_ratios["company_growth"])
        return None

    @classmethod
    def create_or_update_statement(cls, data: dict, financial_model, period=None) -> type:
        # TODO maybe remove the if statement and try to always have a period to avoid repeating
        # statements
        if period:
            statement, created = financial_model.update_or_create(period=period, defaults=data)
            return statement
        return financial_model.create(**data)

    @log_company()
    def create_or_update_inc_statements(self, data: dict, period=None)-> type:
        return self.create_or_update_statement(data, self.company.inc_statements, period)

    @log_company()
    def create_or_update_balance_sheets(self, data: dict, period=None)-> type:
        return self.create_or_update_statement(data, self.company.balance_sheets, period)

    @log_company()
    def create_or_update_cf_statements(self, data: dict, period=None)-> type:
        return self.create_or_update_statement(data, self.company.cf_statements, period)

    @log_company()
    def create_or_update_current_stock_price(self, price):
        return self.company.stock_prices.create(price=price)

    @log_company()
    def create_or_update_rentability_ratios(self, data: dict, period=None)-> type:
        return self.create_or_update_statement(data, self.company.rentability_ratios, period)

    @log_company()
    def create_or_update_liquidity_ratio(self, data: dict, period=None)-> type:
        return self.create_or_update_statement(data, self.company.liquidity_ratios, period)

    @log_company()
    def create_or_update_margin_ratio(self, data: dict, period=None)-> type:
        return self.create_or_update_statement(data, self.company.margins, period)

    @log_company()
    def create_or_update_fcf_ratio(self, data: dict, period=None)-> type:
        return self.create_or_update_statement(data, self.company.fcf_ratios, period)

    @log_company()
    def create_or_update_ps_value(self, data: dict, period=None)-> type:
        return self.create_or_update_statement(data, self.company.per_share_values, period)

    @log_company()
    def create_or_update_non_gaap(self, data: dict, period=None)-> type:
        return self.create_or_update_statement(data, self.company.non_gaap_figures, period)

    @log_company()
    def create_or_update_operation_risk_ratio(self, data: dict, period=None)-> type:
        return self.create_or_update_statement(data, self.company.operation_risks_ratios, period)

    @log_company()
    def create_or_update_enterprise_value_ratio(self, data: dict, period=None)-> type:
        return self.create_or_update_statement(data, self.company.ev_ratios, period)

    @log_company()
    def create_or_update_company_growth(self, data: dict, period=None)-> type:
        return self.create_or_update_statement(data, self.company.growth_rates, period)

    @log_company()
    def create_or_update_efficiency_ratio(self, data: dict, period=None)-> type:
        return self.create_or_update_statement(data, self.company.efficiency_ratios, period)

    @log_company()
    def create_or_update_price_to_ratio(self, data: dict, period=None)-> type:
        return self.create_or_update_statement(data, self.company.price_to_ratios, period)
