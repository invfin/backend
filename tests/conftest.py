import pytest

from bfet import DjangoTestingModel

from apps.socialmedias import constants as social_constants
from apps.web import constants as web_constants
from apps.business.models import (
    Customer,
    Product,
    ProductComment,
    ProductComplementary,
    ProductComplementaryPaymentLink,
    ProductDiscount,
    StripeWebhookResponse,
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
from apps.preguntas_respuestas.models import *
from apps.public_blog.models import *
from apps.web.models import WebsiteEmail, WebsiteEmailsType
from apps.seo.models import *

from apps.recsys.models import *
from apps.screener.models import *
from apps.socialmedias.models import DefaultContent, DefaultTilte, Emoji
from apps.super_investors.models import *
from apps.roboadvisor.models import *
from apps.users.models import *
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


@pytest.fixture(scope="session")
def company(db) -> Company:
    return DjangoTestingModel.create(Company)


# Web exclusive
@pytest.fixture
def web_filters():
    return {"for_content": social_constants.WEB, "purpose": web_constants.CONTENT_FOR_ENGAGEMENT}


@pytest.fixture(scope="function")
def web_title(django_db_blocker, web_filters):
    with django_db_blocker.unblock():
        return DjangoTestingModel.create(DefaultTilte, title=DjangoTestingModel.create_random_string(10), **web_filters)


@pytest.fixture(scope="function")
def web_content(django_db_blocker, web_filters):
    with django_db_blocker.unblock():
        return DjangoTestingModel.create(
            DefaultContent, title=DjangoTestingModel.create_random_string(10), **web_filters
        )


@pytest.fixture(scope="function")
def web_emojis(django_db_blocker):
    with django_db_blocker.unblock():
        return DjangoTestingModel.create(
            Emoji,
            2,
            emoji=DjangoTestingModel.create_random_string(10),
        )
