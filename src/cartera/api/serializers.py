from decimal import Decimal

from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.serializers import (
    CharField,
    DateField,
    DecimalField,
    Field,
    FileField,
    IntegerField,
    ModelSerializer,
    PrimaryKeyRelatedField,
    Serializer,
    StringRelatedField,
    ValidationError,
)

from ..models import (
    CashflowMovementCategory,
    Income,
    Investment,
    Savings,
    Spendings,
)
from ..parse_transactions_file import FileTransactionsHandler


class TransactionsFromFileSerializer(Serializer):
    origin = CharField(max_length=100)
    transactions_file = FileField(allow_empty_file=False)

    def create(self, validated_data):
        user = self.context["request"].user
        # TODO: make it a celery task. Return 201 if the file is saved correctly and 500 if error saving the file
        # once the file saved, parse it and so on
        # Or maybe we should take a look at the file, see if it means something.
        # first we'll focus on firsttrade. It seems that is always the same, at least I asume that.
        # Later on lets try to parse bank statements.
        origin = validated_data.pop("origin", "")
        return FileTransactionsHandler(origin).create(**validated_data, user=user)


class GenericForeignKeyField(Field):
    def to_representation(self, obj):
        print(obj.__dict__)
        print("*" * 100)
        return {
            "content_type_id": obj.content_type.id,
            "object_id": obj.object_id,
        }

    def to_internal_value(self, data):
        # Deserialize the dictionary and create a GenericForeignKey instance
        content_type_id = data.get("content_type_id")
        object_id = data.get("object_id")

        try:
            content_type = ContentType.objects.get(id=content_type_id)
            return content_type.get_object_for_this_type(id=object_id)
        except ContentType.DoesNotExist:
            raise ValidationError("Invalid content_type_id")
        except ObjectDoesNotExist:
            raise ValidationError("Object does not exist")


class CashflowMovementSerializer(ModelSerializer):
    name = CharField(max_length=100, label="Nombre")
    amount = DecimalField(
        max_digits=100,
        decimal_places=2,
        default=Decimal(0.0),
        label="Monto",
    )
    description = CharField(default="", label="Descripción")
    date = DateField(allow_null=True, required=False, label="Fecha del movimiento")
    currency = StringRelatedField()


class InvestmentMovementSerializer(CashflowMovementSerializer):
    quantity = IntegerField(label="Cantidad")
    price = DecimalField(
        max_digits=100,
        decimal_places=2,
        default=Decimal(0.0),
        label="Precio",
    )
    content_type = PrimaryKeyRelatedField(
        queryset=ContentType.objects.all(),
        allow_null=True,
        required=False,
        label="Content Type",
    )
    object_id = IntegerField(allow_null=True, required=False, label="Object ID")
    object = GenericForeignKeyField()


class InvestmentSerializer(InvestmentMovementSerializer):
    class Meta:
        model = Investment
        include = "__all__"


class CashflowMovementCategorySerializer(ModelSerializer):
    class Meta:
        model = CashflowMovementCategory
        include = "__all__"


class IncomeSerializer(CashflowMovementSerializer):
    class Meta:
        model = Income
        include = "__all__"


class SpendingsSerializer(CashflowMovementSerializer):
    class Meta:
        model = Spendings
        include = "__all__"


class SavingsSerializer(CashflowMovementSerializer):
    class Meta:
        model = Savings
        include = "__all__"
