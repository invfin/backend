from typing import Type
from datetime import datetime

from django.conf import settings

from apps.translate.google_trans_new import google_translator
from apps.empresas.models import (
    CompanyUpdateLog,
    InstitutionalOrganization,
    TopInstitutionalOwnership,
)
from apps.empresas.utils import log_company
from apps.empresas.company.ratios import CalculateCompanyFinancialRatios
from apps.empresas.company.retrieve_data import RetrieveCompanyData


IMAGEKIT_URL_ENDPOINT = settings.IMAGEKIT_URL_ENDPOINT
IMAGE_KIT = settings.IMAGE_KIT


class UpdateCompany(CalculateCompanyFinancialRatios, RetrieveCompanyData):
    def __init__(self, company: Type["Company"]) -> None:
        super().__init__()
        self.company: Type["Company"] = company

    def get_most_recent_price(self) -> float:
        if 'currentPrice' in self..info:
            current_price = self..info['currentPrice']
        else:
            current_price = self..financial_data['currentPrice']
        return {'currentPrice':current_price}

    @log_company
    def add_logo(self):
        self.company.image = self..info['logo_url']
        self.company.has_logo = True
        self.company.save(update_fields=['has_logo', 'image'])

    @log_company
    def add_description(self):
        self.company.description = google_translator().translate(self.company.description, lang_src='en', lang_tgt='es')
        self.company.description_translated = True
        self.company.save(update_fields=['description_translated', 'description'])

    def general_update(self):
        if self.company.has_logo is False:
            self.add_logo()
        if self.company.description_translated is False:
            self.add_description()

    def financial_update(self):
        log_message = 'all right'
        try:
            if self.check_last_filing() == 'need update':
                try:
                    finprep_data = self.retreive_data.request_finprep_financials()

                    all_ratios = self.calculate_all_ratios(
                        finprep_data["income_statements"],
                        finprep_data["balance_sheets"],
                        finprep_data["cashflow_statements"]
                    )
                except Exception as e:
                    log_message = e
                    self.company.has_error = True
                    self.company.error_message = e
                    self.company.save(update_fields=['has_error', 'error_message'])
                else:
                    try:
                        self.create_all_ratios(all_ratios)
                        self.company.updated = True
                        self.company.last_update = datetime.now()
                        self.company.save(update_fields=['updated', 'last_update'])
                    except Exception as e:
                        log_message = e
                        CompanyUpdateLog.objects.create_log(self.company, 'second_step_financial_update', log_message)
                        self.company.has_error = True
                        self.company.error_message = e
                        self.company.save(update_fields=['has_error', 'error_message'])
                    finally:
                        CompanyUpdateLog.objects.create_log(self.company, 'first_step_financial_update', log_message)
                finally:
                    CompanyUpdateLog.objects.create_log(self.company, 'first_step_financial_update', log_message)
            else:
                from apps.empresas.tasks import update_company_financials_task
                self.company.date_updated = True
                self.company.save(update_fields=['date_updated'])
                update_company_financials_task.delay()
        except Exception as e:
            log_message = e
            self.company.has_error = True
            self.company.error_message = e
            self.company.save(update_fields=['has_error', 'error_message'])
        finally:
            CompanyUpdateLog.objects.create_log(self.company, 'last_step_financial_update', log_message)

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
    def check_last_filing(self):
        least_recent_date = self.yq_company.balance_sheet()
        least_recent_date = least_recent_date['asOfDate'].max().value // 10**9 # normalize time
        least_recent_year = datetime.fromtimestamp(least_recent_date).year
        if least_recent_year != self.company.most_recent_year:
            return 'need update'
        return 'updated'

    def generate_current_data(
        self,
        income_statements: list,
        balance_sheets: list,
        cashflow_statements: list
    )-> dict:

        current_data = {}
        current_price = self.get_most_recent_price()
        current_income_statements = income_statements[0]
        current_balance_sheets = balance_sheets[0]
        current_cashflow_statements = cashflow_statements[0]
        current_fecha = {
            'date': current_income_statements['calendarYear'],
            'year': current_income_statements['date'],
        }
        current_data.update(current_price)
        current_data.update(current_income_statements)
        current_data.update(current_balance_sheets)
        current_data.update(current_cashflow_statements)
        current_data.update(current_fecha)

        return current_data

    def generate_last_year_data(
        self,
        income_statements: list,
        balance_sheets: list,
        cashflow_statements: list
    )-> dict:

        ly_data = {}
        ly_income_statements = income_statements[1]
        ly_balance_sheets = balance_sheets[1]
        ly_cashflow_statements = cashflow_statements[1]
        ly_fecha = {
            'date': ly_income_statements['calendarYear'],
            'year': ly_income_statements['date'],
        }
        ly_data.update(ly_income_statements)
        ly_data.update(ly_balance_sheets)
        ly_data.update(ly_cashflow_statements)
        ly_data.update(ly_fecha)

        return self.last_year_data(ly_data)



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
