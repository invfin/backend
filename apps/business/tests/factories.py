from model_bakery import baker

from apps.users.tests.factories import regular_user

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


baker.make(Customer)
baker.make(Product)
baker.make(ProductComment)
baker.make(ProductComplementary)
baker.make(ProductComplementaryPaymentLink)
baker.make(ProductDiscount)
baker.make(ProductSubscriber)
baker.make(StripeFields)
baker.make(StripeWebhookResponse)
baker.make(TransactionHistorial)