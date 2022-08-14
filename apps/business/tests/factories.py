from apps.bfet import ExampleModel

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


ExampleModel.create(Customer)
ExampleModel.create(Product)
ExampleModel.create(ProductComment)
ExampleModel.create(ProductComplementary)
ExampleModel.create(ProductComplementaryPaymentLink)
ExampleModel.create(ProductDiscount)
ExampleModel.create(ProductSubscriber)
ExampleModel.create(StripeFields)
ExampleModel.create(StripeWebhookResponse)
ExampleModel.create(TransactionHistorial)
