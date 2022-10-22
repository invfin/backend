# import pytest
# import datetime

# from typing import Dict, Union
# from bfet import DjangoTestingModel

# from apps.socialmedias import constants as social_constants
# from apps.web import constants as web_constants
# from apps.api.models import Key
# from apps.business.models import (
#     Customer,
#     Product,
#     ProductComment,
#     ProductComplementary,
#     ProductComplementaryPaymentLink,
#     ProductDiscount,
#     ProductSubscriber,
#     TransactionHistorial,
# )
# from apps.cartera.models import (
#     Asset,
#     FinancialObjectif,
#     Income,
#     Patrimonio,
#     PositionMovement,
#     Spend,
# )
# from apps.empresas.models import (
#     Company,
#     Exchange,
#     ExchangeOrganisation,
#     IncomeStatement,
#     BalanceSheet,
#     CashflowStatement,
# )
# from apps.escritos.models import (
#     Term,
#     TermContent,
#     TermCorrection,
#     TermsComment,
#     TermsRelatedToResume,
# )

# # from apps.preguntas_respuestas.models import *
# # from apps.public_blog.models import *
# # from apps.web.models import WebsiteEmail, WebsiteEmailsType
# # from apps.seo.models import *

# # from apps.recsys.models import *
# # from apps.screener.models import *
# from apps.socialmedias.models import DefaultContent, DefaultTilte, Emoji

# from apps.super_investors.models import Superinvestor

# # from apps.roboadvisor.models import *
# from apps.users.models import User
# from apps.general.models import (
#     Category,
#     Country,
#     Currency,
#     EmailNotification,
#     Industry,
#     Notification,
#     Sector,
#     Tag,
#     Period,
# )

# from tests.data import *
# from apps.general import constants as general_constants
# from tests.data import escritos_data
# from tests.data import superinvestors_data

# """
# function
# --------
#     Passing django_db_blocker as param avoids to use @pytest.mark.django_db
#     and be allowed to use it for more than a function, otherwise use db

# @pytest.fixture
# ---------------
#     :param scope
#         function:
#             The default scope, the fixture is destroyed at the end of the test.

#         class:
#             The fixture is destroyed during the teardown of the last test in the class.

#         module:
#             The fixture is destroyed during teardown of the last test in the module.

#         package:
#             The fixture is destroyed during teardown of the last test in the package.

#         session:
#             The fixture is destroyed at the end of the test session.

# TODO
# Check if all fixtures are required to be used in session, class or maybe function is enought
# """


# # General
# @pytest.fixture(scope="session", autouse=True)
# def currency(django_db_blocker) -> Currency:
#     with django_db_blocker.unblock():
#         currency = DjangoTestingModel.create(Currency)
#         yield currency
#         currency.delete()


# # Users
# @pytest.fixture(scope="session", autouse=True)
# def user_key_sub(django_db_blocker) -> User:
#     with django_db_blocker.unblock():
#         user_key_sub = DjangoTestingModel.create(User)
#         yield user_key_sub
#         user_key_sub.delete()


# @pytest.fixture(scope="session", autouse=True)
# def user_key(django_db_blocker) -> User:
#     with django_db_blocker.unblock():
#         user_key = DjangoTestingModel.create(User)
#         yield user_key
#         user_key.delete()


# @pytest.fixture(scope="session", autouse=True)
# def user_key_removed(django_db_blocker) -> User:
#     with django_db_blocker.unblock():
#         user_key_removed = DjangoTestingModel.create(User)
#         yield user_key_removed
#         user_key_removed.delete()


# # Business
# @pytest.fixture(scope="session", autouse=True)
# def customer(django_db_blocker, user_key_sub) -> Customer:
#     with django_db_blocker.unblock():
#         customer = DjangoTestingModel.create(Customer, user=user_key_sub)
#         yield customer
#         customer.delete()


# @pytest.fixture(scope="session", autouse=True)
# def product(django_db_blocker) -> Product:
#     with django_db_blocker.unblock():
#         product = DjangoTestingModel.create(Product, title="Excel", slug="excel", is_active=True)
#         yield product
#         product.delete()


# @pytest.fixture(scope="session", autouse=True)
# def product_complementary(django_db_blocker, product, currency) -> ProductComplementary:
#     with django_db_blocker.unblock():
#         product_complementary = DjangoTestingModel.create(
#             ProductComplementary, title="Subscripción excel", product=product, is_active=True, currency=currency
#         )
#         yield product_complementary
#         product_complementary.delete()


# @pytest.fixture(scope="session", autouse=True)
# def product_subscriber(django_db_blocker, product, product_complementary, user_key_sub) -> ProductSubscriber:
#     with django_db_blocker.unblock():
#         product_subscriber = DjangoTestingModel.create(
#             ProductSubscriber,
#             product=product,
#             product_complementary=product_complementary,
#             subscriber=user_key_sub,
#             is_active=True,
#         )
#         yield product_subscriber
#         product_subscriber.delete()


# # Api
# @pytest.fixture(scope="session", autouse=True)
# def key(django_db_blocker, user_key) -> Key:
#     with django_db_blocker.unblock():
#         key = DjangoTestingModel.create(Key, user=user_key, in_use=True, removed=None)
#         yield key
#         key.delete()


# @pytest.fixture(scope="session", autouse=True)
# def subscription_key(django_db_blocker, user_key_sub, product_subscriber) -> Key:
#     with django_db_blocker.unblock():
#         subscription_key = DjangoTestingModel.create(
#             Key, user=user_key_sub, in_use=True, removed=None, subscription=product_subscriber
#         )
#         yield subscription_key
#         subscription_key.delete()


# @pytest.fixture(scope="session", autouse=True)
# def removed_key(django_db_blocker, user_key_removed) -> Key:
#     with django_db_blocker.unblock():
#         removed_key = DjangoTestingModel.create(
#             Key, user=user_key_removed, in_use=False, removed=datetime.datetime.utcnow()
#         )
#         yield removed_key
#         removed_key.delete()


# # Empresas
# @pytest.fixture(scope="class")
# def sector(django_db_blocker) -> Sector:
#     with django_db_blocker.unblock():
#         sector = DjangoTestingModel.create(Sector)
#         yield sector
#         sector.delete()


# @pytest.fixture(scope="class")
# def industry(django_db_blocker) -> Industry:
#     with django_db_blocker.unblock():
#         industry = DjangoTestingModel.create(Industry)
#         yield industry
#         industry.delete()


# @pytest.fixture(scope="class")
# def exchange_org_fr(django_db_blocker) -> ExchangeOrganisation:
#     with django_db_blocker.unblock():
#         exchange_org_fr = DjangoTestingModel.create(ExchangeOrganisation, name="France")
#         yield exchange_org_fr
#         exchange_org_fr.delete()


# @pytest.fixture(scope="class")
# def exchange_org_usa(django_db_blocker) -> ExchangeOrganisation:
#     with django_db_blocker.unblock():
#         exchange_org_usa = DjangoTestingModel.create(ExchangeOrganisation, name="Estados Unidos")
#         yield exchange_org_usa
#         exchange_org_usa.delete()


# @pytest.fixture(scope="class")
# def exchange_nyse(django_db_blocker, exchange_org_usa) -> Exchange:
#     with django_db_blocker.unblock():
#         exchange_nyse = DjangoTestingModel.create(Exchange, exchange_ticker="NYSE", main_org=exchange_org_usa)
#         yield exchange_nyse
#         exchange_nyse.delete()


# @pytest.fixture(scope="class")
# def exchange_euro(django_db_blocker, exchange_org_fr) -> Exchange:
#     with django_db_blocker.unblock():
#         exchange_euro = DjangoTestingModel.create(Exchange, exchange_ticker="EURO", main_org=exchange_org_fr)
#         yield exchange_euro
#         exchange_euro.delete()


# @pytest.fixture(scope="class")
# def apple(django_db_blocker, sector, industry, exchange_nyse) -> Company:
#     with django_db_blocker.unblock():
#         apple = DjangoTestingModel.create(
#             Company,
#             ticker="AAPL",
#             no_incs=False,
#             no_bs=False,
#             no_cfs=False,
#             sector=sector,
#             industry=industry,
#             description_translated=True,
#             updated=False,
#             has_error=True,
#             exchange=exchange_nyse,
#             checkings={"has_institutionals": {"state": "no", "time": ""}},
#         )
#         yield apple
#         apple.delete()


# @pytest.fixture(scope="class")
# def zinga(django_db_blocker, sector, industry, exchange_nyse) -> Company:
#     with django_db_blocker.unblock():
#         zinga = DjangoTestingModel.create(
#             Company,
#             ticker="ZNGA",
#             no_incs=False,
#             no_bs=False,
#             no_cfs=False,
#             sector=sector,
#             industry=industry,
#             description_translated=False,
#             updated=True,
#             has_error=False,
#             exchange=exchange_nyse,
#             checkings={"has_institutionals": {"state": "yes", "time": ""}},
#         )
#         yield zinga
#         zinga.delete()


# @pytest.fixture(scope="class")
# def louis(django_db_blocker, industry, exchange_euro) -> Company:
#     with django_db_blocker.unblock():
#         louis = DjangoTestingModel.create(
#             Company,
#             ticker="LVMH",
#             no_incs=True,
#             no_bs=False,
#             no_cfs=False,
#             industry=industry,
#             description_translated=False,
#             exchange=exchange_euro,
#             updated=False,
#             has_error=False,
#             checkings={"has_institutionals": {"state": "no", "time": ""}},
#         )
#         yield louis
#         louis.delete()


# @pytest.fixture(scope="class")
# def google(django_db_blocker, sector, industry, exchange_nyse) -> Company:
#     with django_db_blocker.unblock():
#         google = DjangoTestingModel.create(
#             Company,
#             ticker="GOOGL",
#             no_incs=False,
#             no_bs=False,
#             no_cfs=False,
#             sector=sector,
#             industry=industry,
#             description_translated=True,
#             exchange=exchange_nyse,
#             updated=False,
#             has_error=False,
#             checkings={"has_institutionals": {"state": "no", "time": ""}},
#         )
#         yield google
#         google.delete()


# @pytest.fixture(scope="class")
# def empresas_manager_companies(django_db_blocker, request, google, apple, zinga, louis, sector, industry) -> None:
#     with django_db_blocker.unblock():
#         request.cls.google = google
#         request.cls.apple = apple
#         request.cls.zinga = zinga
#         request.cls.louis = louis
#         request.cls.sector = sector
#         request.cls.industry = industry
#         yield


# @pytest.fixture(scope="class", autouse=True)
# def clean_company(django_db_blocker) -> Company:
#     with django_db_blocker.unblock():
#         clean_company = DjangoTestingModel.create(
#             Company,
#             name="Intel",
#             ticker="INTC",
#             no_incs=False,
#             no_bs=False,
#             no_cfs=False,
#             description_translated=True,
#             has_logo=True,
#             has_error=False,
#         )
#         yield clean_company
#         clean_company.delete()


# @pytest.fixture(scope="class")
# def poster_clean_company(request, clean_company) -> Company:
#     request.cls.clean_company = clean_company


# @pytest.fixture()
# def period_for_year(django_db_blocker) -> Period:
#     with django_db_blocker.unblock():
#         period_for_year = DjangoTestingModel.create(Period, year=2022, period=general_constants.PERIOD_FOR_YEAR)
#         yield period_for_year
#         period_for_year.delete()


# @pytest.fixture(scope="session")
# def yearly_income_statement(django_db_blocker, clean_company, period_for_year) -> IncomeStatement:
#     """
#     Company: Intel (INTC)
#     Period: For year (2022)
#     """
#     with django_db_blocker.unblock():
#         yearly_income_statement = DjangoTestingModel.create(
#             IncomeStatement, is_ttm=False, company=clean_company, period=period_for_year
#         )
#         yield yearly_income_statement
#         yearly_income_statement.delete()


# @pytest.fixture(scope="session")
# def yearly_balance_sheet(django_db_blocker, clean_company, period_for_year) -> BalanceSheet:
#     """
#     Company: Intel (INTC)
#     Period: For year (2022)
#     """
#     with django_db_blocker.unblock():
#         yearly_balance_sheet = DjangoTestingModel.create(
#             BalanceSheet, is_ttm=False, company=clean_company, period=period_for_year
#         )
#         yield yearly_balance_sheet
#         yearly_balance_sheet.delete()


# @pytest.fixture(scope="session")
# def yearly_cashflow_statement(django_db_blocker, clean_company, period_for_year) -> CashflowStatement:
#     """
#     Company: Intel (INTC)
#     Period: For year (2022)
#     """
#     with django_db_blocker.unblock():
#         yearly_cashflow_statement = DjangoTestingModel.create(
#             CashflowStatement, is_ttm=False, company=clean_company, period=period_for_year
#         )
#         yield yearly_cashflow_statement
#         yearly_cashflow_statement.delete()


# # Escritos
# @pytest.fixture(scope="function")
# def term_and_content(django_db_blocker) -> Term:
#     with django_db_blocker.unblock():
#         term = DjangoTestingModel.create(
#             Term, **escritos_data.TERM, author=DjangoTestingModel.create(User, username="Lucas Montes")
#         )
#         for escrito in escritos_data.TERM_CONTENT:
#             DjangoTestingModel.create(TermContent, **escrito)
#         yield term
#         term.delete()


# @pytest.fixture(scope="function")
# def various_terms(django_db_blocker) -> Term:
#     with django_db_blocker.unblock():
#         author = DjangoTestingModel.create(User, username="Lucas Montes")
#         term_1 = DjangoTestingModel.create(
#             Term,
#             id=1,
#             title="Precio valor contable (P/B)",
#             slug="precio-valor-en-libros",
#             resume=(
#                 "El price to book compara el precio de mercado de una empresa con su valor en libros, que muestra"
#                 " esencialmente el valor dado por el mercado por cada dólar del patrimonio neto de la compañía."
#             ),
#             non_thumbnail_url="/static/general/assets/img/general/why-us.webp",
#             total_votes=0,
#             total_views=238,
#             times_shared=0,
#             author=author,
#         )
#         term_2 = DjangoTestingModel.create(
#             Term,
#             id=2,
#             title="El balance sheet",
#             slug="el-balance-sheet-en-espanol",
#             resume=(
#                 "El balance general es el estado financiero que muestra los activos, los pasivos y el patrimonio de los"
#                 " accionistas."
#             ),
#             non_thumbnail_url=(
#                 "https://cdn.wallstreetmojo.com/wp-content/uploads/2019/11/Comparative-Balance-Sheet-Example-1.1-1.png"
#             ),
#             total_votes=0,
#             total_views=180,
#             times_shared=0,
#             author=author,
#         )
#         yield author
#         yield term_1
#         yield term_2
#         author.delete()
#         term_1.delete()
#         term_2.delete()


# # Superinvestors
# @pytest.fixture()
# def superinvestor(django_db_blocker) -> Superinvestor:
#     with django_db_blocker.unblock():
#         for super_data in superinvestors_data.LIST_SUPERINVESTORS:
#             DjangoTestingModel.create(Superinvestor, **super_data)


# # Web
# @pytest.fixture
# def web_filters() -> Dict[str, Union[int, str]]:
#     return {"for_content": social_constants.WEB, "purpose": web_constants.CONTENT_FOR_ENGAGEMENT}


# @pytest.fixture(scope="function")
# def web_title(django_db_blocker, web_filters) -> DefaultTilte:
#     with django_db_blocker.unblock():
#         web_title = DjangoTestingModel.create(
#             DefaultTilte, title=DjangoTestingModel.create_random_string(10), **web_filters
#         )
#         yield web_title
#         web_title.delete()


# @pytest.fixture(scope="function")
# def web_content(django_db_blocker, web_filters) -> DefaultContent:
#     with django_db_blocker.unblock():
#         web_content = DjangoTestingModel.create(
#             DefaultContent, title=DjangoTestingModel.create_random_string(10), **web_filters
#         )
#         yield web_content
#         web_content.delete()


# @pytest.fixture(scope="function")
# def web_emojis(django_db_blocker) -> Emoji:
#     with django_db_blocker.unblock():
#         web_emojis = DjangoTestingModel.create(
#             Emoji,
#             2,
#             emoji=DjangoTestingModel.create_random_string(10),
#         )
#         yield web_emojis
#         web_emojis.delete()
