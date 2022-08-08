from factory import SubFactory
from factory.django import DjangoModelFactory

from apps.general.models import Country, Sector
from apps.general.tests.data import SECTORS, COUNTRIES
from apps.empresas.company.update import UpdateCompany
from apps.empresas.models import (
    Company,
    Exchange,
    ExchangeOrganisation,
    IncomeStatement
)
from apps.socialmedias.tests.data import AAPL
from apps.empresas.tests.data import INCOME_STATEMENT, BALANCE_SHEET, CASHFLOW_STATEMENT

class AppleExample:

    def create_company(self):
        Country.objects.get_or_create(**COUNTRIES[0])
        Sector.objects.get_or_create(**SECTORS[0])
        company = Company.objects.create(**AAPL)
        return company

    def include_fianancials(self):
        company = self.create_company()
        update_company = UpdateCompany(company)
        for inc in INCOME_STATEMENT:
            update_company.create_income_statement(inc)
        for bs in BALANCE_SHEET:
            update_company.create_balance_sheet(bs)
        for cf in CASHFLOW_STATEMENT:
            update_company.create_cashflow_statement(cf)
        update_company.create_all_ratios(
            update_company.calculate_all_ratios(
                INCOME_STATEMENT,
                BALANCE_SHEET,
                CASHFLOW_STATEMENT
            )
        )
        return company

    @classmethod
    def return_example(cls):
        return cls().include_fianancials()


class ExchangeOrganisationFactory(DjangoModelFactory):
    name = 'Estados Unidos'

    class Meta:
        model = ExchangeOrganisation


class ExchangeFactory(DjangoModelFactory):
    exchange_ticker = 'NYSE'
    exchange = 'New York'
    main_org = SubFactory(ExchangeOrganisationFactory)

    class Meta:
        model = Exchange


class CompanyFactory(DjangoModelFactory):
    ticker = 'AAPL'
    exchange = SubFactory(ExchangeFactory)

    class Meta:
        model = Company


class IncomeStatementFactory(DjangoModelFactory):
    company = SubFactory(CompanyFactory)
    date = 2017

    class Meta:
        model = IncomeStatement
