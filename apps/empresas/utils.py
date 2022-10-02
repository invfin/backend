import json

from django.utils import timezone

import numpy as np
from dateutil.relativedelta import relativedelta

from apps.general import constants
from apps.general.models import Period
from apps.empresas.constants import DEFAULT_JSON_CHECKS_FILE
from apps.empresas.models import Company, CompanyUpdateLog


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
                    company.modify_checkings(checking, has_it)

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
        if company_statements:
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


def add_new_default_check(checking):
    with open(DEFAULT_JSON_CHECKS_FILE, "r") as read_checks_json:
        checks_json = json.load(read_checks_json)
    checks_json.update({f"has_{checking}": {"state": "no", "time": ""}})
    with open(DEFAULT_JSON_CHECKS_FILE, "w") as writte_checks_json:
        json.dump(checks_json, writte_checks_json, indent=2, separators=(",", ": "))
