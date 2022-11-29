import json

from typing import Tuple
from dateutil.relativedelta import relativedelta
from datetime import datetime

import numpy as np

from django.utils import timezone

from apps.general import constants
from apps.periods.models import Period
from apps.empresas.constants import MAX_REQUESTS_FINPREP
from apps.empresas.models import Company, CompanyUpdateLog


class FinprepRequestCheck:
    # TODO see if convert that to a decorator to save some seconds
    def check_remaining_requests(
        self,
        number_requests_to_do: int,
        last_request_time_timestamp: float,
        number_requests_done: int,
    ) -> Tuple:
        now = timezone.now()
        my_tmz = timezone.get_default_timezone()
        if (now - datetime.fromtimestamp(last_request_time_timestamp, tz=my_tmz)).total_seconds() > 86400:
            requests_done = number_requests_to_do
            is_auth = True
        else:
            remianing_requests = MAX_REQUESTS_FINPREP - number_requests_done
            is_auth = number_requests_to_do <= remianing_requests
            requests_done = number_requests_to_do + number_requests_done

        return is_auth, datetime.timestamp(now), requests_done

    def manage_track_requests(self, number_requests_to_do: int) -> bool:
        finprep_requests_done_file = "apps/empresas/parse/finprep_requests_done.json"
        with open(finprep_requests_done_file, "r") as read_checks_json:
            checks_json = json.load(read_checks_json)
            is_auth, last_request, requests_done = self.check_remaining_requests(
                number_requests_to_do,
                checks_json["last_request"],
                checks_json["requests_done"],
            )
            checks_json["requests_done"] = requests_done
            checks_json["last_request"] = last_request
        with open(finprep_requests_done_file, "w") as writte_checks_json:
            json.dump(checks_json, writte_checks_json, indent=2, separators=(",", ": "))
        return is_auth


def detect_outlier(list_data):
    outliers = []
    threshold = 3
    mean_1 = np.mean(list_data)
    std_1 = np.std(list_data)

    for y in list_data:
        z_score = (y - mean_1) / std_1
        if np.abs(z_score) > threshold:
            outliers.append(y)

    if not outliers:
        return "No outliers"
    return outliers


def log_company(checking: str = None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            company = args[0].company
            try:
                func(*args, **kwargs)
                error_message = "Works great"
                had_error = False
            except Exception as e:
                error_message = f"{e}"
                had_error = True
            finally:
                CompanyUpdateLog.objects.create(
                    company=company,
                    date=timezone.now(),
                    where=func.__name__,
                    had_error=had_error,
                    error_message=error_message,
                )
                if checking:
                    has_it = had_error is False
                    company.modify_checking(checking, has_it)

        return wrapper

    return decorator


def arrange_quarters(company):
    """
    TODO
    Fix the try except for when a aurater isn't correctly set becasuse the month is different
    """
    statements_models = [
        company.incomestatementyahooquery_set,
        company.balancesheetyahooquery_set,
        company.cashflowstatementyahooquery_set,
        company.incomestatementyfinance_set,
        company.balancesheetyfinance_set,
        company.cashflowstatementyfinance_set,
    ]
    for statement_obj in statements_models:
        company_statements = statement_obj.all().order_by("year")
        if company_statements and company_statements.filter(period_period=constants.PERIOD_FOR_YEAR).exists():
            for statement in company_statements:
                try:
                    if statement.period.period == constants.PERIOD_FOR_YEAR:
                        date_quarter_4 = statement.year
                        date_quarter_1 = date_quarter_4 + relativedelta(months=+3) + relativedelta(years=+1)
                        date_quarter_2 = date_quarter_1 + relativedelta(months=+3) + relativedelta(years=-1)
                        date_quarter_3 = date_quarter_2 + relativedelta(months=+3)
                        period_dict = {
                            date_quarter_4.month: Period.objects.get_or_create(
                                year=date_quarter_4.year, period=constants.PERIOD_4_QUARTER
                            )[0],
                            date_quarter_1.month: Period.objects.get_or_create(
                                year=date_quarter_1.year, period=constants.PERIOD_1_QUARTER
                            )[0],
                            date_quarter_2.month: Period.objects.get_or_create(
                                year=date_quarter_2.year, period=constants.PERIOD_2_QUARTER
                            )[0],
                            date_quarter_3.month: Period.objects.get_or_create(
                                year=date_quarter_3.year, period=constants.PERIOD_3_QUARTER
                            )[0],
                        }
                    else:
                        statement.period = period_dict[statement.year.month]
                        statement.save(update_fields=["period"])
                except KeyError:
                    statement.period = None
                    statement.save(update_fields=["period"])


def company_searched(search, request):
    empresa_ticker = search.split(" [")[1]
    ticker = empresa_ticker[:-1]
    try:
        empresa_busqueda = Company.objects.get(ticker=ticker)
        redirect_path = empresa_busqueda.get_absolute_url()
    except Exception as e:
        redirect_path = request.META.get("HTTP_REFERER")
    finally:
        return redirect_path
