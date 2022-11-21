from django.conf import settings
from django.core.mail import send_mail
from django.db.models import OuterRef, Q, Subquery

from celery import shared_task

from apps.empresas.models import Company
from apps.empresas.outils.retrieve_data import RetrieveCompanyData
from apps.empresas.outils.update import UpdateCompany
from apps.empresas.utils import arrange_quarters
from apps.periods.constants import PERIOD_FOR_YEAR
from apps.periods.models import Period


class CompanyTask:
    def __init__(self, checking: str, tasks_map_selector: str):
        self.checking: str = checking
        self.tasks_map_selector: str = tasks_map_selector

    def retrieve_company(self):
        return Company.objects.filter_checking_not_seen(self.checking).first()

    def prepare_task(self):
        company = self.retrieve_company()
        if not company:
            return self.send_ending_message()
        return company

    def select_task(self, company):
        retrieve_data = RetrieveCompanyData(company)
        tasks_map = {
            "financials_yfinance_info": self.yfinance_tasks,
            "financials_yahooquery_info": self.yahoo_query_tasks,
            "financials_finprep_info": UpdateCompany(company).create_financials_finprep(),
            "financials_finnhub_info": retrieve_data.create_financials_finnhub,
            "key_stats": retrieve_data.create_key_stats_yahooquery,
            "institutionals": retrieve_data.create_institutionals_yahooquery,
        }
        if (
            self.tasks_map_selector == "financials_yfinance_info"
            or self.tasks_map_selector == "financials_yahooquery_info"
        ):
            return tasks_map[self.tasks_map_selector](retrieve_data)
        return tasks_map[self.tasks_map_selector]()

    def send_ending_message(self):
        return send_mail(
            f"No companies left to check for {self.checking}",
            f"All companies have info for {self.checking}",
            f"InvFin - Automatic <{settings.EMAIL_DEFAULT}>",
            [f"InvFin - Automatic <{settings.EMAIL_DEFAULT}>"],
        )

    def yahoo_query_tasks(self, retrieve_data):
        retrieve_data.create_financials_yahooquery("a")
        retrieve_data.create_financials_yahooquery("q")

    def yfinance_tasks(self, retrieve_data):
        retrieve_data.create_financials_yfinance("a")
        retrieve_data.create_financials_yfinance("q")

    def launch_task(self):
        company = self.prepare_task()
        self.select_task(company)
        # arrange_quarters_task.delay(company.id)


@shared_task()
def create_averages_task(company_id):
    """
    Creates the average statement for a given company according to their last quarterly financials statements
    """
    company = Company.objects.get(id=company_id)
    for period in Period.objects.quarterly_periods():
        if not company.inc_statements.filter(period=period).exists():
            UpdateCompany(company).update_average_financials_statements(period)


@shared_task()
def create_ttm_task(company_id):
    company = Company.objects.get(id=company_id)
    UpdateCompany(company).create_or_update_ttm()


@shared_task()
def arrange_quarters_task(company_id):
    company = Company.objects.get(id=company_id)
    arrange_quarters(company)


@shared_task()
def update_periods_final_statements(company_id):
    """
    Loops over the company statements and update their period to match the FY acording to the statement year
    """
    company = Company.objects.get(id=company_id)
    for statement in company.inc_statements.filter(period__isnull=True, is_ttm=False):
        period, created = Period.objects.get_or_create(year=statement.date, period=PERIOD_FOR_YEAR)
        statement.period = period
        statement.save(update_fields=["period"])
    for statement_manager in [
        company.balance_sheets,
        company.cf_statements,
        company.rentability_ratios,
        company.liquidity_ratios,
        company.margins,
        company.fcf_ratios,
        company.per_share_values,
        company.non_gaap_figures,
        company.operation_risks_ratios,
        company.ev_ratios,
        company.growth_rates,
        company.efficiency_ratios,
        company.price_to_ratios,
    ]:
        statement_manager.filter(period__isnull=True, is_ttm=False).update(
            period_id=Subquery(Period.objects.filter(year=OuterRef("date"), period=PERIOD_FOR_YEAR).only("id"))
        )


@shared_task()
def update_company_key_stats_task():
    CompanyTask("key_stats", "key_stats").launch_task()


@shared_task()
def update_company_institutionals_task():
    CompanyTask("institutionals", "institutionals").launch_task()


@shared_task()
def update_company_financials_finprep_task():
    CompanyTask("fixed_last_finprep", "financials_finprep_info").launch_task()


@shared_task()
def update_company_financials_finnhub_task():
    CompanyTask("first_financials_finnhub_info", "financials_finnhub_info").launch_task()


@shared_task()
def update_company_financials_yfinance_task():
    CompanyTask("first_financials_yfinance_info", "financials_yfinance_info").launch_task()


@shared_task()
def update_company_financials_yahooquery_task():
    CompanyTask("first_financials_yahooquery_info", "financials_yahooquery_info").launch_task()
