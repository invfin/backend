from datetime import datetime

import yahooquery as yq
import yfinance as yf
from django.conf import settings

from apps.empresas.models import (
    CompanyUpdateLog,
    InstitutionalOrganization,
    TopInstitutionalOwnership,
)
from apps.general.models import Currency
from apps.translate.google_trans_new import google_translator

from .ratios import CalculateCompanyFinancialRatios
from .retrieve_data import RetrieveCompanyData


IMAGEKIT_URL_ENDPOINT = settings.IMAGEKIT_URL_ENDPOINT
IMAGE_KIT = settings.IMAGE_KIT


class UpdateCompany(CalculateCompanyFinancialRatios):
    def __init__(self, company) -> None:
        self.company = company
        self.ticker = self.company.ticker
        self.retreive_data = RetrieveCompanyData(self.ticker)
        self.yf_company = yf.Ticker(self.ticker)
        self.yq_company = yq.Ticker(self.ticker)

    def get_most_recent_price(self) -> float:
        if 'currentPrice' in self.yf_company.info:
            current_price = self.yf_company.info['currentPrice']
        else:
            current_price = self.yq_company.financial_data['currentPrice']
        return {'currentPrice':current_price}

    def add_logo(self):
        try:
            self.company.image = self.yf_company.info['logo_url']
            self.company.has_logo = True
            self.company.save(update_fields=['has_logo', 'image'])
            log_message = 'all right'
        except Exception as e:
            log_message = e
        finally:
            CompanyUpdateLog.objects.create_log(self.company, 'add_logo', log_message)

    def save_logo_remotely(self):
        try:
            sector = 'Sin-sector'
            if self.company.sector.sector:
                sector = f'{self.company.sector.sector}'
            imagekit_url = IMAGE_KIT.upload_file(
                file= self.company.image, # required
                file_name= f"{self.company.ticker}.webp", # required
                options= {
                    "folder" : f"/companies/{sector}/",
                "tags": [
                    self.company.ticker, self.company.exchange.exchange,
                    self.company.country.country, self.company.sector.sector,
                    self.company.industry.industry
                    ],
                    "is_private_file": False,
                    "use_unique_file_name": False,
                }
            )
            image = imagekit_url['response']['url']
            imagekit_url = IMAGE_KIT.url({
                "src": image,
                "transformation": [{"height": "300", "width": "300"}],
            })
            self.company.remote_image_imagekit = imagekit_url
            self.company.save(update_fields=['remote_image_imagekit'])
            log_message = 'all right'
        except Exception as e:
            log_message = e
        finally:
            state = 'no'
            if log_message == 'all right':
                state = 'yes'
            self.company.modify_checkings('has_meta_image', state)
            CompanyUpdateLog.objects.create_log(self.company, 'save_logo_remotely', log_message)

    def add_description(self):
        try:
            self.company.description = google_translator().translate(self.company.description, lang_src='en', lang_tgt='es')
            self.company.description_translated = True
            self.company.save(update_fields=['description_translated', 'description'])
            log_message = 'all right'
        except Exception as e:
            log_message = e
        finally:
            CompanyUpdateLog.objects.create_log(self.company, 'add_description', log_message)

    def general_update(self):
        if self.company.has_logo is False:
            self.add_logo()
        if self.company.description_translated is False:
            self.add_description()
        if self.company.has_logo is True and not self.company.remote_image_imagekit:
            self.save_logo_remotely()

    def financial_update(self):
        log_message = 'all right'
        try:
            if self.check_last_filing() == 'need update':
                try:
                    finprep_data = self.retreive_data.request_finprep()

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

    def create_income_statement(self, inc_stt:dict):
        income_statement = self.company.inc_statements.create(
            date = inc_stt['calendarYear'],
            year = inc_stt['date'],
            reported_currency = Currency.objects.get_or_create(currency=inc_stt['reportedCurrency'])[0],
            revenue = inc_stt['revenue'],
            cost_of_revenue = inc_stt['costOfRevenue'],
            gross_profit = inc_stt['grossProfit'],
            rd_expenses = inc_stt['researchAndDevelopmentExpenses'],
            general_administrative_expenses = inc_stt['generalAndAdministrativeExpenses'],
            selling_marketing_expenses = inc_stt['sellingAndMarketingExpenses'],
            sga_expenses = inc_stt['sellingGeneralAndAdministrativeExpenses'],
            other_expenses = inc_stt['otherExpenses'],
            operating_expenses = inc_stt['operatingExpenses'],
            cost_and_expenses = inc_stt['costAndExpenses'],
            interest_expense = inc_stt['interestExpense'],
            depreciation_amortization = inc_stt['depreciationAndAmortization'],
            ebitda = inc_stt['ebitda'],
            operating_income = inc_stt['operatingIncome'],
            net_total_other_income_expenses = inc_stt['totalOtherIncomeExpensesNet'],
            income_before_tax = inc_stt['incomeBeforeTax'],
            income_tax_expenses = inc_stt['incomeTaxExpense'],
            net_income = inc_stt['netIncome'],
            weighted_average_shares_outstanding = inc_stt['weightedAverageShsOut'],
            weighted_average_diluated_shares_outstanding = inc_stt['weightedAverageShsOutDil'],)

        return income_statement

    def create_balance_sheet(self, bal_sht:dict):
        balance_sheet = self.company.balance_sheets.create(
            date = bal_sht['calendarYear'],
            year = bal_sht['date'],
            reported_currency = Currency.objects.get_or_create(currency=bal_sht['reportedCurrency'])[0],
            cash_and_cash_equivalents = bal_sht['cashAndCashEquivalents'],
            short_term_investments = bal_sht['shortTermInvestments'],
            cash_and_short_term_investements = bal_sht['cashAndShortTermInvestments'],
            net_receivables = bal_sht['netReceivables'],
            inventory = bal_sht['inventory'],
            other_current_assets = bal_sht['otherCurrentAssets'],
            total_current_assets = bal_sht['totalCurrentAssets'],
            property_plant_equipement = bal_sht['propertyPlantEquipmentNet'],
            goodwill = bal_sht['goodwill'],
            intangible_assets = bal_sht['intangibleAssets'],
            goodwill_and_intangible_assets = bal_sht['goodwillAndIntangibleAssets'],
            long_term_investments = bal_sht['longTermInvestments'],
            tax_assets = bal_sht['taxAssets'],
            other_non_current_assets = bal_sht['otherNonCurrentAssets'],
            total_non_current_assets = bal_sht['totalNonCurrentAssets'],
            other_assets = bal_sht['otherAssets'],
            total_assets = bal_sht['totalAssets'],
            account_payables = bal_sht['accountPayables'],
            short_term_debt = bal_sht['short_term_debt'],
            tax_payables = bal_sht['tax_payables'],
            deferred_revenue = bal_sht['deferred_revenue'],
            other_current_liabilities = bal_sht['otherCurrentLiabilities'],
            total_current_liabilities = bal_sht['totalCurrentLiabilities'],
            long_term_debt = bal_sht['longTermDebt'],
            deferred_revenue_non_current = bal_sht['deferred_revenueNonCurrent'],
            deferred_tax_liabilities_non_current = bal_sht['deferredTaxLiabilitiesNonCurrent'],
            other_non_current_liabilities = bal_sht['otherNonCurrentLiabilities'],
            total_non_current_liabilities = bal_sht['totalNonCurrentLiabilities'],
            other_liabilities = bal_sht['otherLiabilities'],
            total_liabilities = bal_sht['totalLiabilities'],
            common_stocks = bal_sht['commonStock'],
            retained_earnings = bal_sht['retainedEarnings'],
            accumulated_other_comprehensive_income_loss = bal_sht['accumulatedOtherComprehensiveIncomeLoss'],
            othertotal_stockholders_equity = bal_sht['othertotalStockholdersEquity'],
            total_stockholders_equity = bal_sht['totalStockholdersEquity'],
            total_liabilities_and_stockholders_equity = bal_sht['totalLiabilitiesAndStockholdersEquity'],
            total_investments = bal_sht['totalInvestments'],
            total_debt = bal_sht['totalDebt'],
            net_debt = bal_sht['netDebt'],)

        return balance_sheet

    def create_cashflow_statement(self, csf_stt:dict):
        cashflow_statement = self.company.cf_statements.create(
            date = csf_stt['calendarYear'],
            year = csf_stt['date'],
            reported_currency = Currency.objects.get_or_create(currency=csf_stt['reportedCurrency'])[0],
            net_income = csf_stt['netIncome'],
            depreciation_amortization = csf_stt['depreciationAndAmortization'],
            deferred_income_tax = csf_stt['deferredIncomeTax'],
            stock_based_compesation = csf_stt['stockBasedCompensation'],
            change_in_working_capital = csf_stt['changeInWorkingCapital'],
            accounts_receivables = csf_stt['accountsReceivables'],
            inventory = csf_stt['inventory'],
            accounts_payable = csf_stt['accountsPayables'],
            other_working_capital = csf_stt['otherWorkingCapital'],
            other_non_cash_items = csf_stt['otherNonCashItems'],
            operating_activities_cf = csf_stt['netCashProvidedByOperatingActivities'],
            investments_property_plant_equipment = csf_stt['investmentsInPropertyPlantAndEquipment'],
            acquisitions_net = csf_stt['acquisitionsNet'],
            purchases_investments = csf_stt['purchasesOfInvestments'],
            sales_maturities_investments = csf_stt['salesMaturitiesOfInvestments'],
            other_investing_activites = csf_stt['otherInvestingActivites'],
            investing_activities_cf = csf_stt['netCashUsedForInvestingActivites'],
            debt_repayment = csf_stt['debtRepayment'],
            common_stock_issued = csf_stt['commonStockIssued'],
            common_stock_repurchased = csf_stt['commonStockRepurchased'],
            dividends_paid = csf_stt['dividendsPaid'],
            other_financing_activities = csf_stt['otherFinancingActivites'],
            financing_activities_cf = csf_stt['netCashUsedProvidedByFinancingActivities'],
            effect_forex_exchange = csf_stt['effectOfForexChangesOnCash'],
            net_change_cash = csf_stt['netChangeInCash'],
            cash_end_period = csf_stt['cashAtEndOfPeriod'],
            cash_beginning_period = csf_stt['cashAtBeginningOfPeriod'],
            operating_cf = csf_stt['operatingCashFlow'],
            capex = csf_stt['capitalExpenditure'],
            fcf = csf_stt['freeCashFlow'],)

        return cashflow_statement

    def create_current_stock_price(self, price):
        stock_prices = self.company.stock_prices.create(price=price)
        return stock_prices

    def create_rentability_ratios(self, data:dict):
        rentability_ratios = self.company.rentability_ratios.create(**data)
        return rentability_ratios

    def create_liquidity_ratio(self, data:dict):
        liquidity_ratios = self.company.liquidity_ratios.create(**data)
        return liquidity_ratios

    def create_margin_ratio(self, data:dict):
        margins = self.company.margins.create(**data)
        return margins

    def create_fcf_ratio(self, data:dict):
        fcf_ratios = self.company.fcf_ratios.create(**data)
        return fcf_ratios

    def create_ps_value(self, data:dict):
        per_share_values = self.company.per_share_values.create(**data)
        return per_share_values

    def create_non_gaap(self, data:dict):
        non_gaap_figures = self.company.non_gaap_figures.create(**data)
        return non_gaap_figures

    def create_operation_risk_ratio(self, data:dict):
        operation_risks_ratios = self.company.operation_risks_ratios.create(**data)
        return operation_risks_ratios

    def create_enterprise_value_ratio(self, data:dict):
        ev_ratios = self.company.ev_ratios.create(**data)
        return ev_ratios

    def create_company_growth(self, data:dict):
        growth_rates = self.company.growth_rates.create(**data)
        return growth_rates

    def create_eficiency_ratio(self, data:dict):
        efficiency_ratios = self.company.efficiency_ratios.create(**data)
        return efficiency_ratios

    def create_price_to_ratio(self, data:dict):
        price_to_ratios = self.company.price_to_ratios.create(**data)
        return price_to_ratios

    def institutional_ownership(self):
        df = self.yq_company.institution_ownership
        df = df.reset_index()
        df = df.drop(columns=['symbol','row','maxAge'])
        try:
            log_message = 'all right'
            for index, data in df.iterrows():
                institution, _ = InstitutionalOrganization.objects.get_or_create(
                    name=data['organization']
                )
                if TopInstitutionalOwnership.objects.filter(
                    year=data['reportDate'],
                    company=self.company,
                    organization=institution,
                ).exists():
                    continue
                TopInstitutionalOwnership.objects.create(
                    date=data['reportDate'][:4],
                    year=data['reportDate'],
                    company=self.company,
                    organization=institution,
                    percentage_held=data['pctHeld'],
                    position=data['position'],
                    value=data['value']
                )
        except Exception as e:
            log_message = e
        finally:
            CompanyUpdateLog.objects.create_log(self.company, 'institutional_ownership', log_message)
            return log_message
