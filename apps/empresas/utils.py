from django.utils import timezone
import json

from apps.general import constants
from apps.seo.models import UserCompanyVisited, VisiteurCompanyVisited
from apps.seo.outils.visiteur_meta import SeoInformation
from apps.empresas.constants import DEFAULT_JSON_CHECKS_FILE
from apps.empresas.models import Company, CompanyUpdateLog


def log_company(checking: str = None):
    """
    TODO
    Add checkings to all needed logs
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            company = args[0].company
            try:
                func(*args, **kwargs)
                error_message = "Works greate"
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
    constants.PERIOD_3_QUARTER
    constants.PERIOD_2_QUARTER
    constants.PERIOD_1_QUARTER
    constants.PERIOD_4_QUARTER


def company_searched(search, request):
    empresa_ticker = search.split(' [')[1]
    ticker = empresa_ticker[:-1]
    try:
        empresa_busqueda = Company.objects.get(ticker = ticker)
        redirect_path = empresa_busqueda.get_absolute_url()
    except Exception as e:
        redirect_path = request.META.get('HTTP_REFERER')

    return redirect_path


def add_new_default_check(checking):
    with open(DEFAULT_JSON_CHECKS_FILE, 'r') as read_checks_json:
        checks_json = json.load(read_checks_json)

    checks_json.update(
        {
            f'has_{checking}': {
                'state': 'no',
                'time': ''
            }
        }
    )

    with open(DEFAULT_JSON_CHECKS_FILE, 'w') as writte_checks_json:
        json.dump(checks_json, writte_checks_json, indent=2, separators=(',',': '))
