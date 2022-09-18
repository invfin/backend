from typing import Type
from datetime import datetime

from apps.translate.google_trans_new import google_translator
from apps.empresas.utils import log_company
from apps.empresas.outils.ratios import CalculateCompanyFinancialRatios
from apps.empresas.outils.average_statements import AverageStatements
from apps.general.constants import PERIOD_FOR_YEAR


class UpdateCompany(CalculateCompanyFinancialRatios, AverageStatements):
    def __init__(self, company: Type["Company"]) -> None:
        self.company: Type["Company"] = company

    def add_logo(self):
        self.company.image = self.request_info_yfinance["logo_url"]
        self.company.has_logo = True
        self.company.save(update_fields=["has_logo", "image"])

    def add_description(self):
        self.company.description = google_translator().translate(self.company.description, lang_src="en", lang_tgt="es")
        self.company.description_translated = True
        self.company.save(update_fields=["description_translated", "description"])

    def general_update(self):
        if not self.company.image:
            self.add_logo()
        if self.company.description_translated is False:
            self.add_description()

    def check_last_filing(self):
        least_recent_date = self.yq_company.balance_sheet()
        least_recent_date = least_recent_date["asOfDate"].max().value // 10**9  # normalize time
        least_recent_year = datetime.fromtimestamp(least_recent_date).year
        if least_recent_year != self.company.most_recent_year:
            return "need update"
        return "updated"

    def update_base_financials_statements(self, period: Type["Period"]):
        for funct_calculate_statement, funct_create_statement in [
            (self.calculate_average_income_statement, self.create_inc_statements),
            (self.calculate_average_balance_sheet, self.create_balance_sheets),
            (self.calculate_average_cashflow_statement, self.create_cf_statements),
        ]:
            averaged_stement = funct_calculate_statement(period)
            if averaged_stement:
                averaged_stement.update({"company": self.company})
                funct_create_statement(averaged_stement)

    def create_ttm(self):
        last_inc_statements = (
            self.company.inc_statements.all().exclude(period=PERIOD_FOR_YEAR).order_by("-period", "year")[:4]
        )
        print(last_inc_statements)
        last_balance_sheets = self.company.balance_sheets.all().exclude(period=PERIOD_FOR_YEAR)[:4]
        last_cf_statements = self.company.cf_statements.all().exclude(period=PERIOD_FOR_YEAR)[:4]

    def create_all_ratios(self, all_ratios: dict):
        self.create_current_stock_price(price=all_ratios["current_data"]["currentPrice"])
        self.create_rentability_ratios(all_ratios["rentability_ratios"])
        self.create_liquidity_ratio(all_ratios["liquidity_ratio"])
        self.create_margin_ratio(all_ratios["margin_ratio"])
        self.create_fcf_ratio(all_ratios["fcf_ratio"])
        self.create_ps_value(all_ratios["ps_value"])
        self.create_non_gaap(all_ratios["non_gaap"])
        self.create_operation_risk_ratio(all_ratios["operation_risk_ratio"])
        self.create_price_to_ratio(all_ratios["price_to_ratio"])
        self.create_enterprise_value_ratio(all_ratios["enterprise_value_ratio"])
        self.create_eficiency_ratio(all_ratios["eficiency_ratio"])
        self.create_company_growth(all_ratios["company_growth"])

    def create_inc_statements(self, data: dict):
        return self.company.inc_statements.create(**data)

    def create_balance_sheets(self, data: dict):
        return self.company.balance_sheets.create(**data)

    def create_cf_statements(self, data: dict):
        return self.company.cf_statements.create(**data)

    def create_current_stock_price(self, price):
        return self.company.stock_prices.create(price=price)

    def create_rentability_ratios(self, data: dict):
        return self.company.rentability_ratios.create(**data)

    def create_liquidity_ratio(self, data: dict):
        return self.company.liquidity_ratios.create(**data)

    def create_margin_ratio(self, data: dict):
        return self.company.margins.create(**data)

    def create_fcf_ratio(self, data: dict):
        return self.company.fcf_ratios.create(**data)

    def create_ps_value(self, data: dict):
        return self.company.per_share_values.create(**data)

    def create_non_gaap(self, data: dict):
        return self.company.non_gaap_figures.create(**data)

    def create_operation_risk_ratio(self, data: dict):
        return self.company.operation_risks_ratios.create(**data)

    def create_enterprise_value_ratio(self, data: dict):
        return self.company.ev_ratios.create(**data)

    def create_company_growth(self, data: dict):
        return self.company.growth_rates.create(**data)

    def create_eficiency_ratio(self, data: dict):
        return self.company.efficiency_ratios.create(**data)

    def create_price_to_ratio(self, data: dict):
        return self.company.price_to_ratios.create(**data)
