import pytest

from bfet import DataCreator, DjangoTestingModel

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
from apps.web.models import *
from apps.seo.models import *

from apps.recsys.models import *
from apps.screener.models import *
from apps.socialmedias.models import *
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
