from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    StringRelatedField,
)

from ..models import (
    Asset,
    Buy,
    Sell,
    CashflowMovementCategory,
    Income,
    Spend,
)


class AssetSerializer(ModelSerializer):
    class Meta:
        model = Asset
        exclude = ["id"]


class BuySerializer(ModelSerializer):
    class Meta:
        model = Buy
        exclude = ["id"]


class SellSerializer(ModelSerializer):
    class Meta:
        model = Sell
        exclude = ["id"]


class CashflowMovementCategorySerializer(ModelSerializer):
    class Meta:
        model = CashflowMovementCategory
        exclude = ["id"]


class IncomeSerializer(ModelSerializer):
    class Meta:
        model = Income
        exclude = ["id"]


class SpendSerializer(ModelSerializer):
    class Meta:
        model = Spend
        exclude = ["id"]
