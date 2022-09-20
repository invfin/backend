from django.core.management import BaseCommand

from apps.empresas.tasks import (
    create_averages_task,
    fix_information_incorrect_filed_task,
    update_periods_final_statements,
    arrange_quarters_task,
    update_finprep_from_current,
    create_ttm_task,
    update_company_financials_yfinance_task,
    update_company_financials_yahooquery_task,
)
from apps.empresas.models import Company


class Command(BaseCommand):
    def handle(self, *args, **options):
        for company in Company.objects.all():
            fix_information_incorrect_filed_task.delay(company.id)
            update_periods_final_statements.delay(company.id)
            update_finprep_from_current.delay(company.id)
            if not company.check_checkings("first_financials_yfinance_info"):
                update_company_financials_yfinance_task.delay(company.id)
            if not company.check_checkings("first_financials_yahooquery_info"):
                update_company_financials_yahooquery_task.delay(company.id)
            create_averages_task(company.id)
            arrange_quarters_task.delay(company.id)
            create_ttm_task.delay(company.id)
