from datetime import datetime

from apps.seo.models import UserCompanyVisited, VisiteurCompanyVisited
from apps.seo.utils import SeoInformation
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
                    date=datetime.now(),
                    where=func.__name__,
                    had_error=had_error,
                    error_message=error_message,
                )
                if checking:
                    has_it = had_error is False
                    company.modify_checkings(checking, has_it)
        return wrapper
    return decorator


def save_search(request, model_visited):
    """
    TODO
    When visiteur will be implemented in the request, retreive the visiteur from there
    """
    if request.user.is_authenticated:
        user = request.user
        save_model = UserCompanyVisited
    else:
        user = SeoInformation().find_visiteur(request)
        save_model = VisiteurCompanyVisited

    save_model.objects.create(
        user=user,
        model_visited=model_visited,
        date=datetime.now()
    )


def company_searched(search, request):
    empresa_ticker = search.split(' [')[1]
    ticker = empresa_ticker[:-1]
    try:
        empresa_busqueda = Company.objects.get(ticker = ticker)
        redirect_path = empresa_busqueda.get_absolute_url()
        save_search(request, empresa_busqueda)
    except Exception as e:
        redirect_path = request.META.get('HTTP_REFERER')

    return redirect_path
