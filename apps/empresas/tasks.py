from datetime import datetime

from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Q

from config import celery_app

from apps.empresas.company.update import UpdateCompany
from apps.empresas.models import Company


@celery_app.task()
def update_institutionals_info_company_task():
    intento = 0
    for org_name in ['Estados Unidos', 'México']:
        companies_without_info = Company.objects.clean_companies_by_main_exchange(org_name)
        for company in companies_without_info:
            if intento == 5:
                return
            if company.check_checkings("has_institutionals") == False:
                update = UpdateCompany(company).institutional_ownership
                if update == 'all right':
                    intento += 1
                    company.modify_checkings('has_institutionals', 'yes')


@celery_app.task()
def update_basic_info_company_task():
    companies_without_info = Company.objects.filter(Q(has_logo=False) | Q(description_translated=False))
    if companies_without_info.exists():
        company = companies_without_info.first()
        return UpdateCompany(company).general_update()
    else:
        return send_mail('No companies left', 'All companies have info', settings.EMAIL_DEFAULT, [settings.EMAIL_DEFAULT])


@celery_app.task()
def update_company_financials_task():
    companies_without_info = Company.objects.clean_companies().filter(date_updated=False)
    if companies_without_info.exists():
        company = companies_without_info.first()
        return UpdateCompany(company).financial_update()
    else:
        return send_mail(
            'No companies left to update financials',
            f'All companies have info for {org_name}',
            settings.EMAIL_DEFAULT,
            [settings.EMAIL_DEFAULT]
        )
