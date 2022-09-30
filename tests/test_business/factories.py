from bfet import DjangoTestingModel as DTM

from apps.business.models import (
Customer,
Product,
ProductComment,
ProductComplementary,
ProductComplementaryPaymentLink,
ProductDiscount,
ProductSubscriber,
StripeFields,
StripeWebhookResponse,
TransactionHistorial,
)


DTM.create(Customer)
DTM.create(Product)
DTM.create(ProductComment)
DTM.create(ProductComplementary)
DTM.create(ProductComplementaryPaymentLink)
DTM.create(ProductDiscount)
DTM.create(ProductSubscriber)
DTM.create(StripeFields)
DTM.create(StripeWebhookResponse)
DTM.create(TransactionHistorial)
