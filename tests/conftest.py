import pytest
import datetime

from typing import Dict, Union, List
from bfet import DjangoTestingModel

from apps.socialmedias import constants as social_constants
from apps.web import constants as web_constants
from apps.api.models import Key
from apps.business.models import (
    Customer,
    Product,
    ProductComment,
    ProductComplementary,
    ProductComplementaryPaymentLink,
    ProductDiscount,
    ProductSubscriber,
    TransactionHistorial,
)
from apps.cartera.models import (
    Asset,
    FinancialObjectif,
    Income,
    Patrimonio,
    PositionMovement,
    Spend,
)
from apps.empresas.models import (
    Company,
    Exchange,
    ExchangeOrganisation,
    IncomeStatement,
    BalanceSheet,
    CashflowStatement,
)
from apps.escritos.models import (
    Term,
    TermContent,
    TermCorrection,
    TermsComment,
    TermsRelatedToResume,
)

from apps.preguntas_respuestas.models import Question, QuesitonComment, Answer, AnswerComment

from apps.public_blog.models import PublicBlog, NewsletterFollowers

# from apps.web.models import WebsiteEmail, WebsiteEmailsType
# from apps.seo.models import *

# from apps.recsys.models import *
# from apps.screener.models import *
from apps.socialmedias.models import DefaultContent, DefaultTilte, Emoji

from apps.super_investors.models import Superinvestor

# from apps.roboadvisor.models import *
from apps.users.models import User, Profile
from apps.general.models import (
    Category,
    Country,
    Currency,
    EmailNotification,
    Industry,
    Notification,
    Sector,
    Tag,
    Period,
)

from tests.data import *
from apps.general import constants as general_constants
from tests.data import escritos_data
from tests.data import superinvestors_data

"""
function
--------
    Passing django_db_blocker as param avoids to use @pytest.mark.django_db
    and be allowed to use it for more than a function, otherwise use db

@pytest.fixture
---------------
    :param scope
        function:
            The default scope, the fixture is destroyed at the end of the test.

        class:
            The fixture is destroyed during the teardown of the last test in the class.

        module:
            The fixture is destroyed during teardown of the last test in the module.

        package:
            The fixture is destroyed during teardown of the last test in the package.

        session:
            The fixture is destroyed at the end of the test session.

TODO
Check if all fixtures are required to be used in session, class or maybe function is enought
"""

# General
@pytest.fixture(scope="session", autouse=True)
def currency(django_db_blocker) -> Currency:
    with django_db_blocker.unblock():
        return DjangoTestingModel.create(Currency)


@pytest.fixture(scope="class")
def notification_system(django_db_blocker, request) -> None:
    with django_db_blocker.unblock():
        request.cls.writter = DjangoTestingModel.create(User, is_writter=True)
        request.cls.user_1 = DjangoTestingModel.create(User)
        request.cls.user_2 = DjangoTestingModel.create(User)
        DjangoTestingModel.create(Profile, user=request.cls.writter)
        DjangoTestingModel.create(Profile, user=request.cls.user_1)
        DjangoTestingModel.create(Profile, user=request.cls.user_2)
        request.cls.question = DjangoTestingModel.create(Question, author=request.cls.user_1)
        request.cls.question_comment = DjangoTestingModel.create(
            QuesitonComment, content_related=DjangoTestingModel.create(Question), author=DjangoTestingModel.create(User)
        )
        request.cls.answer = DjangoTestingModel.create(
            Answer, author=DjangoTestingModel.create(User), question_related=request.cls.question
        )
        request.cls.answer_comment = DjangoTestingModel.create(
            AnswerComment,
            author=DjangoTestingModel.create(User),
            content_related=DjangoTestingModel.create(
                Answer,
                author=DjangoTestingModel.create(User),
                question_related=DjangoTestingModel.create(Question, author=DjangoTestingModel.create(User)),
            ),
        )
        request.cls.followers = DjangoTestingModel.create(NewsletterFollowers, user=request.cls.writter)
        request.cls.blog = DjangoTestingModel.create(PublicBlog, author=request.cls.writter)
        request.cls.followers.followers.add(request.cls.user_1)
        yield


# Users
@pytest.fixture(scope="session", autouse=True)
def user_key_sub(django_db_blocker) -> User:
    with django_db_blocker.unblock():
        return DjangoTestingModel.create(User)


@pytest.fixture(scope="session", autouse=True)
def user_key(django_db_blocker) -> User:
    with django_db_blocker.unblock():
        return DjangoTestingModel.create(User)


@pytest.fixture(scope="session", autouse=True)
def user_key_removed(django_db_blocker) -> User:
    with django_db_blocker.unblock():
        return DjangoTestingModel.create(User)


# Business
@pytest.fixture(scope="session", autouse=True)
def customer(django_db_blocker, user_key_sub) -> Customer:
    with django_db_blocker.unblock():
        return DjangoTestingModel.create(Customer, user=user_key_sub)


@pytest.fixture(scope="session", autouse=True)
def product(django_db_blocker) -> Product:
    with django_db_blocker.unblock():
        return DjangoTestingModel.create(Product, title="Excel", slug="excel", is_active=True)


@pytest.fixture(scope="session", autouse=True)
def product_complementary(django_db_blocker, product, currency) -> ProductComplementary:
    with django_db_blocker.unblock():
        return DjangoTestingModel.create(
            ProductComplementary, title="Subscripción excel", product=product, is_active=True, currency=currency
        )


@pytest.fixture(scope="session", autouse=True)
def product_subscriber(django_db_blocker, product, product_complementary, user_key_sub) -> ProductSubscriber:
    with django_db_blocker.unblock():
        return DjangoTestingModel.create(
            ProductSubscriber,
            product=product,
            product_complementary=product_complementary,
            subscriber=user_key_sub,
            is_active=True,
        )


# Api
@pytest.fixture(scope="session", autouse=True)
def key(django_db_blocker, user_key) -> Key:
    with django_db_blocker.unblock():
        return DjangoTestingModel.create(Key, user=user_key, in_use=True, removed=None)


@pytest.fixture(scope="session", autouse=True)
def subscription_key(django_db_blocker, user_key_sub, product_subscriber) -> Key:
    with django_db_blocker.unblock():
        return DjangoTestingModel.create(
            Key, user=user_key_sub, in_use=True, removed=None, subscription=product_subscriber
        )


@pytest.fixture(scope="session", autouse=True)
def removed_key(django_db_blocker, user_key_removed) -> Key:
    with django_db_blocker.unblock():
        return DjangoTestingModel.create(Key, user=user_key_removed, in_use=False, removed=datetime.datetime.utcnow())


# Empresas
@pytest.fixture(scope="class")
def sector(django_db_blocker) -> Sector:
    with django_db_blocker.unblock():
        return DjangoTestingModel.create(Sector)


@pytest.fixture(scope="class")
def industry(django_db_blocker) -> Industry:
    with django_db_blocker.unblock():
        return DjangoTestingModel.create(Industry)


@pytest.fixture(scope="class")
def exchange_org_fr(django_db_blocker) -> ExchangeOrganisation:
    with django_db_blocker.unblock():
        return DjangoTestingModel.create(ExchangeOrganisation, name="France")


@pytest.fixture(scope="class")
def exchange_org_usa(django_db_blocker) -> ExchangeOrganisation:
    with django_db_blocker.unblock():
        return DjangoTestingModel.create(ExchangeOrganisation, name="Estados Unidos")


@pytest.fixture(scope="class")
def exchange_nyse(django_db_blocker, exchange_org_usa) -> Exchange:
    with django_db_blocker.unblock():
        return DjangoTestingModel.create(Exchange, exchange_ticker="NYSE", main_org=exchange_org_usa)


@pytest.fixture(scope="class")
def exchange_euro(django_db_blocker, exchange_org_fr) -> Exchange:
    with django_db_blocker.unblock():
        return DjangoTestingModel.create(Exchange, exchange_ticker="EURO", main_org=exchange_org_fr)


@pytest.fixture(scope="class")
def apple(django_db_blocker, sector, industry, exchange_nyse) -> Company:
    with django_db_blocker.unblock():
        return DjangoTestingModel.create(
            Company,
            ticker="AAPL",
            no_incs=False,
            no_bs=False,
            no_cfs=False,
            sector=sector,
            industry=industry,
            description_translated=True,
            updated=False,
            has_error=True,
            exchange=exchange_nyse,
            checkings={"has_institutionals": {"state": "no", "time": ""}},
        )


@pytest.fixture(scope="class")
def zinga(django_db_blocker, sector, industry, exchange_nyse) -> Company:
    with django_db_blocker.unblock():
        return DjangoTestingModel.create(
            Company,
            ticker="ZNGA",
            no_incs=False,
            no_bs=False,
            no_cfs=False,
            sector=sector,
            industry=industry,
            description_translated=False,
            updated=True,
            has_error=False,
            exchange=exchange_nyse,
            checkings={"has_institutionals": {"state": "yes", "time": ""}},
        )


@pytest.fixture(scope="class")
def louis(django_db_blocker, industry, exchange_euro) -> Company:
    with django_db_blocker.unblock():
        return DjangoTestingModel.create(
            Company,
            ticker="LVMH",
            no_incs=True,
            no_bs=False,
            no_cfs=False,
            industry=industry,
            description_translated=False,
            exchange=exchange_euro,
            updated=False,
            has_error=False,
            checkings={"has_institutionals": {"state": "no", "time": ""}},
        )


@pytest.fixture(scope="class")
def google(django_db_blocker, sector, industry, exchange_nyse) -> Company:
    with django_db_blocker.unblock():
        return DjangoTestingModel.create(
            Company,
            ticker="GOOGL",
            no_incs=False,
            no_bs=False,
            no_cfs=False,
            sector=sector,
            industry=industry,
            description_translated=True,
            exchange=exchange_nyse,
            updated=False,
            has_error=False,
            checkings={"has_institutionals": {"state": "no", "time": ""}},
        )


@pytest.fixture(scope="class")
def empresas_manager_companies(django_db_blocker, request, google, apple, zinga, louis, sector, industry) -> None:
    with django_db_blocker.unblock():
        request.cls.google = google
        request.cls.apple = apple
        request.cls.zinga = zinga
        request.cls.louis = louis
        request.cls.sector = sector
        request.cls.industry = industry
        yield


@pytest.fixture()
def clean_company(django_db_blocker) -> Company:
    with django_db_blocker.unblock():
        return DjangoTestingModel.create(
            Company,
            name="Intel",
            ticker="INTC",
            no_incs=False,
            no_bs=False,
            no_cfs=False,
            description_translated=True,
            has_logo=True,
            has_error=False,
        )


@pytest.fixture()
def period_for_year(django_db_blocker) -> Period:
    with django_db_blocker.unblock():
        return DjangoTestingModel.create(Period, year=2022, period=general_constants.PERIOD_FOR_YEAR)


@pytest.fixture(scope="session")
def yearly_income_statement(django_db_blocker, clean_company, period_for_year) -> IncomeStatement:
    """
    Company: Intel (INTC)
    Period: For year (2022)
    """
    with django_db_blocker.unblock():
        return DjangoTestingModel.create(IncomeStatement, is_ttm=False, compny=clean_company, period=period_for_year)


@pytest.fixture(scope="session")
def yearly_balance_sheet(django_db_blocker, clean_company, period_for_year) -> BalanceSheet:
    """
    Company: Intel (INTC)
    Period: For year (2022)
    """
    with django_db_blocker.unblock():
        return DjangoTestingModel.create(BalanceSheet, is_ttm=False, compny=clean_company, period=period_for_year)


@pytest.fixture(scope="session")
def yearly_cashflow_statement(django_db_blocker, clean_company, period_for_year) -> CashflowStatement:
    """
    Company: Intel (INTC)
    Period: For year (2022)
    """
    with django_db_blocker.unblock():
        return DjangoTestingModel.create(CashflowStatement, is_ttm=False, compny=clean_company, period=period_for_year)


# Escritos
@pytest.fixture(scope="function")
def term_and_content(django_db_blocker) -> Term:
    with django_db_blocker.unblock():
        term = DjangoTestingModel.create(
            Term, **escritos_data.TERM, author=DjangoTestingModel.create(User, username="Lucas Montes")
        )
        for escrito in escritos_data.TERM_CONTENT:
            DjangoTestingModel.create(TermContent, **escrito)
        return term


@pytest.fixture(scope="function")
def various_terms(django_db_blocker) -> Term:
    with django_db_blocker.unblock():
        author = DjangoTestingModel.create(User, username="Lucas Montes")
        DjangoTestingModel.create(
            Term,
            id=1,
            title="Precio valor contable (P/B)",
            slug="precio-valor-en-libros",
            resume=(
                "El price to book compara el precio de mercado de una empresa con su valor en libros, que muestra"
                " esencialmente el valor dado por el mercado por cada dólar del patrimonio neto de la compañía."
            ),
            non_thumbnail_url="/static/general/assets/img/general/why-us.webp",
            total_votes=0,
            total_views=238,
            times_shared=0,
            author=author,
        )
        DjangoTestingModel.create(
            Term,
            id=2,
            title="El balance sheet",
            slug="el-balance-sheet-en-espanol",
            resume=(
                "El balance general es el estado financiero que muestra los activos, los pasivos y el patrimonio de los"
                " accionistas."
            ),
            non_thumbnail_url=(
                "https://cdn.wallstreetmojo.com/wp-content/uploads/2019/11/Comparative-Balance-Sheet-Example-1.1-1.png"
            ),
            total_votes=0,
            total_views=180,
            times_shared=0,
            author=author,
        )
        yield


# Superinvestors
@pytest.fixture()
def superinvestor(django_db_blocker) -> Superinvestor:
    with django_db_blocker.unblock():
        for super_data in superinvestors_data.LIST_SUPERINVESTORS:
            DjangoTestingModel.create(Superinvestor, **super_data)


# Web
@pytest.fixture
def web_filters() -> Dict[str, Union[int, str]]:
    return {"for_content": social_constants.WEB, "purpose": web_constants.CONTENT_FOR_ENGAGEMENT}


@pytest.fixture(scope="function")
def web_title(django_db_blocker, web_filters) -> DefaultTilte:
    with django_db_blocker.unblock():
        return DjangoTestingModel.create(DefaultTilte, title=DjangoTestingModel.create_random_string(10), **web_filters)


@pytest.fixture(scope="function")
def web_content(django_db_blocker, web_filters) -> DefaultContent:
    with django_db_blocker.unblock():
        return DjangoTestingModel.create(
            DefaultContent, title=DjangoTestingModel.create_random_string(10), **web_filters
        )


@pytest.fixture(scope="function")
def web_emojis(django_db_blocker) -> Emoji:
    with django_db_blocker.unblock():
        return DjangoTestingModel.create(
            Emoji,
            2,
            emoji=DjangoTestingModel.create_random_string(10),
        )
