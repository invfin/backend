from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    StringRelatedField,
)

from src.empresas.models import (
    BalanceSheet,
    CashflowStatement,
    Company,
    CompanyGrowth,
    CompanyStockPrice,
    EficiencyRatio,
    EnterpriseValueRatio,
    Exchange,
    ExchangeOrganisation,
    FreeCashFlowRatio,
    IncomeStatement,
    LiquidityRatio,
    MarginRatio,
    NonGaap,
    OperationRiskRatio,
    PerShareValue,
    PriceToRatio,
    RentabilityRatio,
)


class ExchangeOrganisationSerializer(ModelSerializer):
    class Meta:
        model = ExchangeOrganisation
        exclude = ["id", "order"]


class ExchangeSerializer(ModelSerializer):
    country = StringRelatedField(many=False)

    class Meta:
        model = Exchange
        exclude = [
            "id",
            "main_org",
            "data_source",
        ]


class BasicCompanySerializer(ModelSerializer):
    exchange = StringRelatedField(many=False)
    currency = StringRelatedField(many=False)
    industry = StringRelatedField(many=False)
    sector = StringRelatedField(many=False)
    country = StringRelatedField(many=False)

    class Meta:
        model = Company
        fields = [
            "ticker",
            "name",
            "currency",
            "industry",
            "sector",
            "website",
            "state",
            "country",
            "ceo",
            "image",
            "city",
            "employees",
            "address",
            "zip_code",
            "cik",
            "exchange",
            "cusip",
            "isin",
            "description",
            "ipoDate",
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)

        # Truncate the description field to a desired length
        max_description_length = 100
        description = data.get("description")
        if description and len(description) > max_description_length:
            data["description"] = f"{description[:max_description_length]}..."

        return data


class CompanyStockPriceSerializer(ModelSerializer):
    class Meta:
        model = CompanyStockPrice
        exclude = ["id", "year"]


class ExcelIncomeStatementSerializer(ModelSerializer):
    reported_currency = StringRelatedField(many=False)

    class Meta:
        model = IncomeStatement
        fields = [
            "date",
            "reported_currency",
            "revenue",
            "cost_of_revenue",
            "gross_profit",
            "rd_expenses",
            "general_administrative_expenses",
            "selling_marketing_expenses",
            "sga_expenses",
            "other_expenses",
            "operating_expenses",
            "cost_and_expenses",
            "interest_expense",
            "depreciation_amortization",
            "ebitda",
            "operating_income",
            "net_total_other_income_expenses",
            "income_before_tax",
            "income_tax_expenses",
            "net_income",
            "weighted_average_shares_outstanding",
            "weighted_average_diluated_shares_outstanding",
        ]


class ExcelBalanceSheetSerializer(ModelSerializer):
    reported_currency = StringRelatedField(many=False)

    class Meta:
        model = BalanceSheet
        fields = [
            "date",
            "reported_currency",
            "cash_and_cash_equivalents",
            "short_term_investments",
            "cash_and_short_term_investments",
            "net_receivables",
            "inventory",
            "other_current_assets",
            "total_current_assets",
            "property_plant_equipment",
            "goodwill",
            "intangible_assets",
            "goodwill_and_intangible_assets",
            "long_term_investments",
            "tax_assets",
            "other_non_current_assets",
            "total_non_current_assets",
            "other_assets",
            "total_assets",
            "accounts_payable",
            "short_term_debt",
            "tax_payables",
            "deferred_revenue",
            "other_current_liabilities",
            "total_current_liabilities",
            "long_term_debt",
            "deferred_revenue_non_current",
            "deferred_tax_liabilities_non_current",
            "other_non_current_liabilities",
            "total_non_current_liabilities",
            "other_liabilities",
            "total_liabilities",
            "common_stocks",
            "retained_earnings",
            "accumulated_other_comprehensive_income_loss",
            "othertotal_stockholders_equity",
            "total_stockholders_equity",
            "total_liabilities_and_total_equity",
            "total_investments",
            "total_debt",
            "net_debt",
        ]


class ExcelCashflowStatementSerializer(ModelSerializer):
    reported_currency = StringRelatedField(many=False)

    class Meta:
        model = CashflowStatement
        fields = [
            "date",
            "reported_currency",
            "net_income",
            "depreciation_amortization",
            "deferred_income_tax",
            "stock_based_compensation",
            "change_in_working_capital",
            "accounts_receivable",
            "inventory",
            "accounts_payable",
            "other_working_capital",
            "other_non_cash_items",
            "operating_activities_cf",
            "investments_property_plant_equipment",
            "acquisitions_net",
            "purchases_investments",
            "sales_maturities_investments",
            "other_investing_activites",
            "investing_activities_cf",
            "debt_repayment",
            "common_stock_issued",
            "common_stock_repurchased",
            "dividends_paid",
            "other_financing_activities",
            "financing_activities_cf",
            "effect_forex_exchange",
            "net_change_cash",
            "cash_end_period",
            "cash_beginning_period",
            "operating_cf",
            "capex",
            "fcf",
        ]


class BaseStatementSerializer(ModelSerializer):
    reported_currency = StringRelatedField(many=False)
    company = StringRelatedField(many=False)

    class Meta:
        exclude = ["id", "year", "is_ttm", "from_average", "period"]


class IncomeStatementSerializer(BaseStatementSerializer):
    class Meta(BaseStatementSerializer.Meta):
        model = IncomeStatement


class BalanceSheetSerializer(BaseStatementSerializer):
    class Meta(BaseStatementSerializer.Meta):
        model = BalanceSheet


class CashflowStatementSerializer(BaseStatementSerializer):
    class Meta(BaseStatementSerializer.Meta):
        model = CashflowStatement


class RentabilityRatioSerializer(BaseStatementSerializer):
    class Meta(BaseStatementSerializer.Meta):
        model = RentabilityRatio


class LiquidityRatioSerializer(BaseStatementSerializer):
    class Meta(BaseStatementSerializer.Meta):
        model = LiquidityRatio


class MarginRatioSerializer(BaseStatementSerializer):
    class Meta(BaseStatementSerializer.Meta):
        model = MarginRatio


class FreeCashFlowRatioSerializer(BaseStatementSerializer):
    class Meta(BaseStatementSerializer.Meta):
        model = FreeCashFlowRatio


class PerShareValueSerializer(BaseStatementSerializer):
    class Meta(BaseStatementSerializer.Meta):
        model = PerShareValue


class NonGaapSerializer(BaseStatementSerializer):
    class Meta(BaseStatementSerializer.Meta):
        model = NonGaap


class OperationRiskRatioSerializer(BaseStatementSerializer):
    class Meta(BaseStatementSerializer.Meta):
        model = OperationRiskRatio


class EnterpriseValueRatioSerializer(BaseStatementSerializer):
    class Meta(BaseStatementSerializer.Meta):
        model = EnterpriseValueRatio


class CompanyGrowthSerializer(BaseStatementSerializer):
    class Meta(BaseStatementSerializer.Meta):
        model = CompanyGrowth


class EficiencyRatioSerializer(BaseStatementSerializer):
    class Meta(BaseStatementSerializer.Meta):
        model = EficiencyRatio


class PriceToRatioSerializer(BaseStatementSerializer):
    class Meta(BaseStatementSerializer.Meta):
        model = PriceToRatio


class CompanySerializer(ModelSerializer):
    averages = SerializerMethodField()
    inc_statements = SerializerMethodField()
    balance_sheets = SerializerMethodField()
    cf_statements = SerializerMethodField()
    rentability_ratios = SerializerMethodField()
    liquidity_ratios = SerializerMethodField()
    margins = SerializerMethodField()
    fcf_ratios = SerializerMethodField()
    per_share_values = SerializerMethodField()
    non_gaap_figures = SerializerMethodField()
    operation_risks_ratios = SerializerMethodField()
    ev_ratios = SerializerMethodField()
    growth_rates = SerializerMethodField()
    efficiency_ratios = SerializerMethodField()
    price_to_ratios = SerializerMethodField()
    exchange = StringRelatedField(many=False)
    currency = StringRelatedField(many=False)
    industry = StringRelatedField(many=False)
    sector = StringRelatedField(many=False)
    country = StringRelatedField(many=False)

    class Meta:
        model = Company
        fields = [
            "averages",
            "ticker",
            "name",
            "currency",
            "industry",
            "sector",
            "website",
            "state",
            "country",
            "ceo",
            "image",
            "city",
            "employees",
            "address",
            "zip_code",
            "cik",
            "exchange",
            "cusip",
            "isin",
            "description",
            "ipoDate",
            "inc_statements",
            "balance_sheets",
            "cf_statements",
            "rentability_ratios",
            "liquidity_ratios",
            "margins",
            "fcf_ratios",
            "per_share_values",
            "non_gaap_figures",
            "operation_risks_ratios",
            "ev_ratios",
            "growth_rates",
            "efficiency_ratios",
            "price_to_ratios",
        ]

    def slicing(self) -> int:
        return 10

    def get_inc_statements(self, obj):
        queryset = obj.inc_statements.year()[: self.slicing()]
        return IncomeStatementSerializer(queryset, many=True).data

    def get_balance_sheets(self, obj):
        queryset = obj.balance_sheets.year()[: self.slicing()]
        return BalanceSheetSerializer(queryset, many=True).data

    def get_cf_statements(self, obj):
        queryset = obj.cf_statements.year()[: self.slicing()]
        return CashflowStatementSerializer(queryset, many=True).data

    def get_rentability_ratios(self, obj):
        queryset = obj.rentability_ratios.year()[: self.slicing()]
        return RentabilityRatioSerializer(queryset, many=True).data

    def get_liquidity_ratios(self, obj):
        queryset = obj.liquidity_ratios.year()[: self.slicing()]
        return LiquidityRatioSerializer(queryset, many=True).data

    def get_margins(self, obj):
        queryset = obj.margins.year()[: self.slicing()]
        return MarginRatioSerializer(queryset, many=True).data

    def get_fcf_ratios(self, obj):
        queryset = obj.fcf_ratios.year()[: self.slicing()]
        return FreeCashFlowRatioSerializer(queryset, many=True).data

    def get_per_share_values(self, obj):
        queryset = obj.per_share_values.year()[: self.slicing()]
        return PerShareValueSerializer(queryset, many=True).data

    def get_non_gaap_figures(self, obj):
        queryset = obj.non_gaap_figures.year()[: self.slicing()]
        return NonGaapSerializer(queryset, many=True).data

    def get_operation_risks_ratios(self, obj):
        queryset = obj.operation_risks_ratios.year()[: self.slicing()]
        return OperationRiskRatioSerializer(queryset, many=True).data

    def get_ev_ratios(self, obj):
        queryset = obj.ev_ratios.year()[: self.slicing()]
        return EnterpriseValueRatioSerializer(queryset, many=True).data

    def get_growth_rates(self, obj):
        queryset = obj.growth_rates.year()[: self.slicing()]
        return CompanyGrowthSerializer(queryset, many=True).data

    def get_efficiency_ratios(self, obj):
        queryset = obj.efficiency_ratios.year()[: self.slicing()]
        return EficiencyRatioSerializer(queryset, many=True).data

    def get_price_to_ratios(self, obj):
        queryset = obj.price_to_ratios.year()[: self.slicing()]
        return PriceToRatioSerializer(queryset, many=True).data

    def get_averages(self, obj):
        averages = Company.objects.get_all_averages(obj.pk, obj.sector)
        return averages
