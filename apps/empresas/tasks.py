from django.conf import settings
from django.core.mail import send_mail
from django.db.models import OuterRef, Subquery, Q

from config import celery_app

from apps.empresas.outils.update import UpdateCompany
from apps.empresas.outils.retrieve_data import RetrieveCompanyData
from apps.general.constants import PERIOD_FOR_YEAR
from apps.general.models import Period
from apps.empresas.models import (
    Company,
    BalanceSheetFinprep,
    IncomeStatementFinprep,
    CashflowStatementFinprep
)

@celery_app.task()
def update_periods_current_average_statements(company_id):
    company = Company.objects.get(id=company_id)
    for statement in company.inc_statements.all():
        period, created = Period.objects.get_or_create(year=statement.date, period=PERIOD_FOR_YEAR)
        statement.period = period
        statement.save(update_fields=["period"])

    company.balance_sheets.all().update(
        period_id=Subquery(
            Period.objects.filter(year=OuterRef("date"), period=PERIOD_FOR_YEAR).only("id")
        )
    )
    company.cf_statements.all().update(
        period_id=Subquery(
            Period.objects.filter(year=OuterRef("date"), period=PERIOD_FOR_YEAR).only("id")
        )
    )
    company.rentability_ratios.all().update(
        period_id=Subquery(
            Period.objects.filter(year=OuterRef("date"), period=PERIOD_FOR_YEAR).only("id")
        )
    )
    company.liquidity_ratios.all().update(
        period_id=Subquery(
            Period.objects.filter(year=OuterRef("date"), period=PERIOD_FOR_YEAR).only("id")
        )
    )
    company.margins.all().update(
        period_id=Subquery(
            Period.objects.filter(year=OuterRef("date"), period=PERIOD_FOR_YEAR).only("id")
        )
    )
    company.fcf_ratios.all().update(
        period_id=Subquery(
            Period.objects.filter(year=OuterRef("date"), period=PERIOD_FOR_YEAR).only("id")
        )
    )
    company.per_share_values.all().update(
        period_id=Subquery(
            Period.objects.filter(year=OuterRef("date"), period=PERIOD_FOR_YEAR).only("id")
        )
    )
    company.non_gaap_figures.all().update(
        period_id=Subquery(
            Period.objects.filter(year=OuterRef("date"), period=PERIOD_FOR_YEAR).only("id")
        )
    )
    company.operation_risks_ratios.all().update(
        period_id=Subquery(
            Period.objects.filter(year=OuterRef("date"), period=PERIOD_FOR_YEAR).only("id")
        )
    )
    company.ev_ratios.all().update(
        period_id=Subquery(
            Period.objects.filter(year=OuterRef("date"), period=PERIOD_FOR_YEAR).only("id")
        )
    )
    company.growth_rates.all().update(
        period_id=Subquery(
            Period.objects.filter(year=OuterRef("date"), period=PERIOD_FOR_YEAR).only("id")
        )
    )
    company.efficiency_ratios.all().update(
        period_id=Subquery(
            Period.objects.filter(year=OuterRef("date"), period=PERIOD_FOR_YEAR).only("id")
        )
    )
    company.price_to_ratios.all().update(
        period_id=Subquery(
            Period.objects.filter(year=OuterRef("date"), period=PERIOD_FOR_YEAR).only("id")
        )
    )


@celery_app.task()
def update_finprep_from_current(company_id):
    company = Company.objects.get(id=company_id)
    for company_data in company.inc_statements.all().values():
        date = company_data["date"]
        period, created = Period.objects.get_or_create(year=date, period=PERIOD_FOR_YEAR)
        company_data.pop("id")
        company_data.pop("is_ttm")
        company_data["period_id"] = period.id
        IncomeStatementFinprep.objects.get_or_create(
            cost_and_expenses=company_data.pop("cost_and_expenses"),
            cost_of_revenue=company_data.pop("cost_of_revenue"),
            depreciation_and_amortization=company_data.pop("depreciation_amortization"),
            ebitda=company_data.pop("ebitda"),
            general_and_administrative_expenses=company_data.pop("general_administrative_expenses"),
            gross_profit=company_data.pop("gross_profit"),
            income_before_tax=company_data.pop("income_before_tax"),
            income_tax_expense=company_data.pop("income_tax_expenses"),
            interest_expense=company_data.pop("interest_expense"),
            net_income=company_data.pop("net_income"),
            operating_expenses=company_data.pop("operating_expenses"),
            operating_income=company_data.pop("operating_income"),
            other_expenses=company_data.pop("other_expenses"),
            research_and_development_expenses=company_data.pop("rd_expenses"),
            revenue=company_data.pop("revenue"),
            selling_and_marketing_expenses=company_data.pop("selling_marketing_expenses"),
            selling_general_and_administrative_expenses=company_data.pop("sga_expenses"),
            total_other_income_expenses_net=company_data.pop("net_total_other_income_expenses"),
            weighted_average_shs_out=company_data.pop("weighted_average_shares_outstanding"),
            weighted_average_shs_out_dil=company_data.pop("weighted_average_diluated_shares_outstanding"),
            **company_data
        )
    for company_data in company.balance_sheets.all().values():
        date = company_data["date"]
        period, created = Period.objects.get_or_create(year=date, period=PERIOD_FOR_YEAR)
        company_data.pop("id")
        company_data.pop("is_ttm")
        company_data["period_id"] = period.id
        BalanceSheetFinprep.objects.get_or_create(
            property_plant_equipment_net=company_data.pop("property_plant_equipment"),
            common_stock=company_data.pop("common_stocks"),
            **company_data
        )
    for company_data in company.cf_statements.all().values():
        date = company_data["date"]
        period, created = Period.objects.get_or_create(year=date, period=PERIOD_FOR_YEAR)
        company_data.pop("id")
        company_data.pop("is_ttm")
        company_data["period_id"] = period.id
        CashflowStatementFinprep.objects.get_or_create(
            depreciation_and_amortization=company_data.pop("depreciation_amortization"),
            stock_based_compensation=company_data.pop("stock_based_compesation"),
            accounts_payables=company_data.pop("accounts_payable"),
            operating_cash_flow=company_data.pop("operating_cf"),
            free_cash_flow=company_data.pop("fcf"),
            capital_expenditure=company_data.pop("capex"),
            net_cash_provided_by_operating_activities=company_data.pop("operating_activities_cf"),
            net_cash_used_for_investing_activites=company_data.pop("investing_activities_cf"),
            net_cash_used_provided_by_financing_activities=company_data.pop("financing_activities_cf"),
            investments_in_property_plant_and_equipment=company_data.pop("investments_property_plant_equipment"),
            purchases_of_investments=company_data.pop("purchases_investments"),
            sales_maturities_of_investments=company_data.pop("sales_maturities_investments"),
            effect_of_forex_changes_on_cash=company_data.pop("effect_forex_exchange"),
            other_financing_activites=company_data.pop("other_financing_activities"),
            net_change_in_cash=company_data.pop("net_change_cash"),
            cash_at_end_of_period=company_data.pop("cash_end_period"),
            cash_at_beginning_of_period=company_data.pop("cash_beginning_period"),
            **company_data
        )


@celery_app.task()
def update_basic_info_company_task():
    companies_without_info = Company.objects.filter(Q(has_logo=False) | Q(description_translated=False))
    if companies_without_info.exists():
        company = companies_without_info.first()
        return UpdateCompany(company).general_update()
    else:
        return send_mail('No companies left', 'All companies have info', settings.EMAIL_DEFAULT, [settings.EMAIL_DEFAULT])


@celery_app.task()
def update_company_key_stats_task():
    companies_without_info = Company.objects.filter_checkings_not_seen("key_stats")
    if companies_without_info.exists():
        company = companies_without_info.first()
        return RetrieveCompanyData(company).create_key_stats_yahooquery()
    else:
        return send_mail(
            'No companies left to update key_stats',
            f'All companies have info for key_stats',
            settings.EMAIL_DEFAULT,
            [settings.EMAIL_DEFAULT]
        )


@celery_app.task()
def update_company_institutionals_task():
    companies_without_info = Company.objects.filter_checkings_not_seen("institutionals")
    if companies_without_info.exists():
        company = companies_without_info.first()
        return RetrieveCompanyData(company).create_institutionals_yahooquery()
    else:
        return send_mail(
            'No companies left to update institutionals',
            f'All companies have info for institutionals',
            settings.EMAIL_DEFAULT,
            [settings.EMAIL_DEFAULT]
        )


@celery_app.task()
def update_company_financials_finprep_task():
    companies_without_info = Company.objects.filter_checkings_not_seen("latest_financials_finprep_info")
    if companies_without_info.exists():
        company = companies_without_info.first()
        return RetrieveCompanyData(company).create_financials_finprep()
    else:
        return send_mail(
            'No companies left to update financials for latest_financials_finprep_info',
            f'All companies have info for latest_financials_finprep_info',
            settings.EMAIL_DEFAULT,
            [settings.EMAIL_DEFAULT]
        )


@celery_app.task()
def update_company_financials_finnhub_task():
    companies_without_info = Company.objects.filter_checkings_not_seen("first_financials_finnhub_info")
    if companies_without_info.exists():
        company = companies_without_info.first()
        return RetrieveCompanyData(company).create_financials_finnhub()
    else:
        return send_mail(
            'No companies left to update financials first_financials_finnhub_info',
            f'All companies have info for first_financials_finnhub_info',
            settings.EMAIL_DEFAULT,
            [settings.EMAIL_DEFAULT]
        )


@celery_app.task()
def update_company_financials_yfinance_task():
    companies_without_info = Company.objects.filter_checkings_not_seen("first_financials_yfinance_info")
    if companies_without_info.exists():
        company = companies_without_info.first()
        RetrieveCompanyData(company).create_financials_yfinance("a")
        RetrieveCompanyData(company).create_financials_yfinance("q")
    else:
        return send_mail(
            'No companies left to update financials for first_financials_yfinance_info',
            f'All companies have info for first_financials_yfinance_info',
            settings.EMAIL_DEFAULT,
            [settings.EMAIL_DEFAULT]
        )


@celery_app.task()
def update_company_financials_yahooquery_task():
    companies_without_info = Company.objects.filter_checkings_not_seen("first_financials_yahooquery_info")
    if companies_without_info.exists():
        company = companies_without_info.first()
        RetrieveCompanyData(company).create_financials_yahooquery("a")
        RetrieveCompanyData(company).create_financials_yahooquery("q")
    else:
        return send_mail(
            'No companies left to update financials ofr first_financials_yahooquery_info',
            f'All companies have info for first_financials_yahooquery_info',
            settings.EMAIL_DEFAULT,
            [settings.EMAIL_DEFAULT]
        )
