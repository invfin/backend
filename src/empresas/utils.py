from datetime import datetime
import json
from typing import Tuple

from django.utils import timezone
from django.db.models import Q

import numpy as np

from src.empresas.constants import MAX_REQUESTS_FINPREP
from src.empresas.models import Company, CompanyUpdateLog
from src.periods import constants
from src.periods.outils import FiscalDate


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
        if (
            now - datetime.fromtimestamp(last_request_time_timestamp, tz=my_tmz)
        ).total_seconds() > 86400:
            requests_done = number_requests_to_do
            is_auth = True
        else:
            remianing_requests = MAX_REQUESTS_FINPREP - number_requests_done
            is_auth = number_requests_to_do <= remianing_requests
            requests_done = number_requests_to_do + number_requests_done

        return is_auth, datetime.timestamp(now), requests_done

    def manage_track_requests(self, number_requests_to_do: int) -> bool:
        try:
            finprep_requests_done_file = "src/empresas/parse/finprep_requests_done.json"
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
        except json.JSONDecodeError:
            return False


def detect_outlier(list_data)->list:
    threshold = 3
    mean_1 = np.mean(list_data)
    std_1 = np.std(list_data)

    outliers = [y for y in list_data if np.abs((y - mean_1) / std_1) > threshold]

    return "No outliers" if not outliers else outliers


def log_company(checking: str = ""):
    """
    Decorator used to log posisble errors when updating a company.
    """

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

            CompanyUpdateLog.objects.create(
                company=company,
                date=timezone.now(),
                where=func.__name__,
                had_error=had_error,
                error_message=error_message,
            )
            if checking:
                company.modify_checking(checking, not had_error)

        return wrapper

    return decorator


def arrange_quarters(company: Company) -> None:
    for statement_obj in [
        company.incomestatementyahooquery_set,
        company.balancesheetyahooquery_set,
        company.cashflowstatementyahooquery_set,
        company.incomestatementyfinance_set,
        company.balancesheetyfinance_set,
        company.cashflowstatementyfinance_set,
    ]:
        for statement in statement_obj.exclude(
            Q(period__period=constants.PERIOD_FOR_YEAR) | ~Q(date=None)
        ):
            fiscal = FiscalDate(statement.year)
            statement.date = fiscal.regular_date.year
            statement.period = fiscal.period
            statement.save(update_fields=["period", "date"])
