from typing import Type
from datetime import datetime

from apps.translate.google_trans_new import google_translator
from apps.empresas.utils import log_company
from apps.empresas.company.ratios import CalculateCompanyFinancialRatios
from apps.empresas.company.retrieve_data import RetrieveCompanyData


class UpdateCompany(CalculateCompanyFinancialRatios, RetrieveCompanyData):
    def __init__(self, company: Type["Company"]) -> None:
        super().__init__(company)
        self.company: Type["Company"] = company

    @log_company
    def add_logo(self):
        self.company.image = self.request_info_yfinance['logo_url']
        self.company.has_logo = True
        self.company.save(update_fields=['has_logo', 'image'])

    @log_company
    def add_description(self):
        self.company.description = google_translator().translate(self.company.description, lang_src='en', lang_tgt='es')
        self.company.description_translated = True
        self.company.save(update_fields=['description_translated', 'description'])

    def general_update(self):
        if not self.company.image:
            self.add_logo()
        if self.company.description_translated is False:
            self.add_description()

    @log_company
    def check_last_filing(self):
        least_recent_date = self.yq_company.balance_sheet()
        least_recent_date = least_recent_date['asOfDate'].max().value // 10**9 # normalize time
        least_recent_year = datetime.fromtimestamp(least_recent_date).year
        if least_recent_year != self.company.most_recent_year:
            return 'need update'
        return 'updated'

    @log_company
    def create_all_ratios(self, all_ratios: dict):
        self.create_current_stock_price(price = all_ratios["current_data"]['currentPrice'])
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

    @log_company
    def create_current_stock_price(self, price):
        return self.company.stock_prices.create(price=price)

    @log_company
    def create_rentability_ratios(self, data:dict):
        return self.company.rentability_ratios.create(**data)

    @log_company
    def create_liquidity_ratio(self, data:dict):
        return self.company.liquidity_ratios.create(**data)

    @log_company
    def create_margin_ratio(self, data:dict):
        return self.company.margins.create(**data)

    @log_company
    def create_fcf_ratio(self, data:dict):
        return self.company.fcf_ratios.create(**data)

    @log_company
    def create_ps_value(self, data:dict):
        return self.company.per_share_values.create(**data)

    @log_company
    def create_non_gaap(self, data:dict):
        return self.company.non_gaap_figures.create(**data)

    @log_company
    def create_operation_risk_ratio(self, data:dict):
        return self.company.operation_risks_ratios.create(**data)

    @log_company
    def create_enterprise_value_ratio(self, data:dict):
        return self.company.ev_ratios.create(**data)

    @log_company
    def create_company_growth(self, data:dict):
        return self.company.growth_rates.create(**data)

    @log_company
    def create_eficiency_ratio(self, data:dict):
        return self.company.efficiency_ratios.create(**data)

    @log_company
    def create_price_to_ratio(self, data:dict):
        return self.company.price_to_ratios.create(**data)
