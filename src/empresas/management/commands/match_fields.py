from django.core.management import BaseCommand

from src.general.models import Period
from src.empresas.models import Company


class Command(BaseCommand):
    def handle(self, *args, **options):
        period = Period.objects.for_year_period(2021)
        company = Company.objects.get(ticker="AAPL")
        # incomestatementyahooquery = company.incomestatementyahooquery_set.get(period=period)
        # balancesheetyahooquery = company.balancesheetyahooquery_set.get(period=period)
        # cashflowstatementyahooquery = company.cashflowstatementyahooquery_set.get(period=period)
        # incomestatementyfinance = company.incomestatementyfinance_set.get(period=period)
        # balancesheetyfinance = company.balancesheetyfinance_set.get(period=period)
        # cashflowstatementyfinance = company.cashflowstatementyfinance_set.get(period=period)
        incomestatementfinprep = company.incomestatementfinprep_set.get(period=period)
        balancesheetfinprep = company.balancesheetfinprep_set.get(period=period)
        cashflowstatementfinprep = company.cashflowstatementfinprep_set.get(period=period)
        inc_statements = company.inc_statements.get(period=period)
        balance_sheets = company.balance_sheets.get(period=period)
        cf_statements = company.cf_statements.get(period=period)
        inc_statements_dict = inc_statements.__dict__
        inc_statements_dict.pop("year")
        inc_statements_dict.pop("_state")
        inc_statements_dict.pop("id")
        inc_statements_dict.pop("date")
        inc_statements_dict.pop("period_id")
        inc_statements_dict.pop("company_id")
        inc_statements_dict.pop("reported_currency_id")
        inc_statements_dict.pop("is_ttm")

        similar = dict()
        for st, nombre in [(incomestatementfinprep, "finprep")]:
            st_dict = st.__dict__
            st_dict.pop("year")
            st_dict.pop("_state")
            st_dict.pop("id")
            st_dict.pop("date")
            st_dict.pop("period_id")
            st_dict.pop("company_id")
            st_dict.pop("reported_currency_id")
            for key, value in st_dict.items():
                for inc_key, inc_value in inc_statements_dict.items():
                    if value == inc_value:
                        if not inc_key in similar:
                            similar[inc_key] = {nombre: key}
                        else:
                            similar[inc_key].update({nombre: key})
