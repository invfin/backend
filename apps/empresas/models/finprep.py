from django.db.models import (
    SET_NULL,
    FloatField,
    ForeignKey,
)

from apps.empresas.models.base import BaseStatement


class IncomeStatementFinprep(BaseStatement):
    reported_currency = ForeignKey("general.Currency", on_delete=SET_NULL, null=True, blank=True)
    revenue = FloatField(default=0, blank=True, null=True)
    cost_of_revenue = FloatField(default=0, blank=True, null=True)
    gross_profit = FloatField(default=0, blank=True, null=True)
    rd_expenses = FloatField(default=0, blank=True, null=True)
    general_administrative_expenses = FloatField(default=0, blank=True, null=True)
    selling_marketing_expenses = FloatField(default=0, blank=True, null=True)
    sga_expenses = FloatField(default=0, blank=True, null=True)
    other_expenses = FloatField(default=0, blank=True, null=True)
    operating_expenses = FloatField(default=0, blank=True, null=True)
    cost_and_expenses = FloatField(default=0, blank=True, null=True)
    interest_expense = FloatField(default=0, blank=True, null=True)
    depreciation_amortization = FloatField(default=0, blank=True, null=True)
    ebitda = FloatField(default=0, blank=True, null=True)
    operating_income = FloatField(default=0, blank=True, null=True)
    net_total_other_income_expenses = FloatField(default=0, blank=True, null=True)
    income_before_tax = FloatField(default=0, blank=True, null=True)
    income_tax_expenses = FloatField(default=0, blank=True, null=True)
    net_income = FloatField(default=0, blank=True, null=True)
    weighted_average_shares_outstanding = FloatField(default=0, blank=True, null=True)
    weighted_average_diluated_shares_outstanding = FloatField(default=0, blank=True, null=True)

    class Meta(BaseStatement.Meta):
        verbose_name = "Finprep Income Statement"
        verbose_name_plural = "Finprep Income Statements"
        db_table = "assets_companies_income_statements_finprep"

    def __str__(self):
        return self.company.ticker + str(self.date)


class BalanceSheetFinprep(BaseStatement):
    reported_currency = ForeignKey("general.Currency", on_delete=SET_NULL, null=True, blank=True)
    cash_and_cash_equivalents = FloatField(default=0, blank=True, null=True)
    short_term_investments = FloatField(default=0, blank=True, null=True)
    cash_and_short_term_investements = FloatField(default=0, blank=True, null=True)
    net_receivables = FloatField(default=0, blank=True, null=True)
    inventory = FloatField(default=0, blank=True, null=True)
    other_current_assets = FloatField(default=0, blank=True, null=True)
    total_current_assets = FloatField(default=0, blank=True, null=True)
    property_plant_equipement = FloatField(default=0, blank=True, null=True)
    goodwill = FloatField(default=0, blank=True, null=True)
    intangible_assets = FloatField(default=0, blank=True, null=True)
    goodwill_and_intangible_assets = FloatField(default=0, blank=True, null=True)
    long_term_investments = FloatField(default=0, blank=True, null=True)
    tax_assets = FloatField(default=0, blank=True, null=True)
    other_non_current_assets = FloatField(default=0, blank=True, null=True)
    total_non_current_assets = FloatField(default=0, blank=True, null=True)
    other_assets = FloatField(default=0, blank=True, null=True)
    total_assets = FloatField(default=0, blank=True, null=True)
    account_payables = FloatField(default=0, blank=True, null=True)
    short_term_debt = FloatField(default=0, blank=True, null=True)
    tax_payables = FloatField(default=0, blank=True, null=True)
    deferred_revenue = FloatField(default=0, blank=True, null=True)
    other_current_liabilities = FloatField(default=0, blank=True, null=True)
    total_current_liabilities = FloatField(default=0, blank=True, null=True)
    long_term_debt = FloatField(default=0, blank=True, null=True)
    deferred_revenue_non_current = FloatField(default=0, blank=True, null=True)
    deferred_tax_liabilities_non_current = FloatField(default=0, blank=True, null=True)
    other_non_current_liabilities = FloatField(default=0, blank=True, null=True)
    total_non_current_liabilities = FloatField(default=0, blank=True, null=True)
    other_liabilities = FloatField(default=0, blank=True, null=True)
    total_liabilities = FloatField(default=0, blank=True, null=True)
    common_stocks = FloatField(default=0, blank=True, null=True)
    retained_earnings = FloatField(default=0, blank=True, null=True)
    accumulated_other_comprehensive_income_loss = FloatField(default=0, blank=True, null=True)
    othertotal_stockholders_equity = FloatField(default=0, blank=True, null=True)
    total_stockholders_equity = FloatField(default=0, blank=True, null=True)
    total_liabilities_and_stockholders_equity = FloatField(default=0, blank=True, null=True)
    total_investments = FloatField(default=0, blank=True, null=True)
    total_debt = FloatField(default=0, blank=True, null=True)
    net_debt = FloatField(default=0, blank=True, null=True)

    class Meta(BaseStatement.Meta):
        verbose_name = "Finprep Balance Sheet"
        verbose_name_plural = "Finprep Balance Sheets"
        db_table = "assets_companies_balance_sheet_statements_finprep"

    def __str__(self):
        return self.company.ticker + str(self.date)


class CashflowStatement(BaseStatement):
    reported_currency = ForeignKey("general.Currency", on_delete=SET_NULL, null=True, blank=True)
    net_income = FloatField(default=0, blank=True, null=True)
    depreciation_amortization = FloatField(default=0, blank=True, null=True)
    deferred_income_tax = FloatField(default=0, blank=True, null=True)
    stock_based_compesation = FloatField(default=0, blank=True, null=True)
    change_in_working_capital = FloatField(default=0, blank=True, null=True)
    accounts_receivables = FloatField(default=0, blank=True, null=True)
    inventory = FloatField(default=0, blank=True, null=True)
    accounts_payable = FloatField(default=0, blank=True, null=True)
    other_working_capital = FloatField(default=0, blank=True, null=True)
    other_non_cash_items = FloatField(default=0, blank=True, null=True)
    operating_activities_cf = FloatField(default=0, blank=True, null=True)
    investments_property_plant_equipment = FloatField(default=0, blank=True, null=True)
    acquisitions_net = FloatField(default=0, blank=True, null=True)
    purchases_investments = FloatField(default=0, blank=True, null=True)
    sales_maturities_investments = FloatField(default=0, blank=True, null=True)
    other_investing_activites = FloatField(default=0, blank=True, null=True)
    investing_activities_cf = FloatField(default=0, blank=True, null=True)
    debt_repayment = FloatField(default=0, blank=True, null=True)
    common_stock_issued = FloatField(default=0, blank=True, null=True)
    common_stock_repurchased = FloatField(default=0, blank=True, null=True)
    dividends_paid = FloatField(default=0, blank=True, null=True)
    other_financing_activities = FloatField(default=0, blank=True, null=True)
    financing_activities_cf = FloatField(default=0, blank=True, null=True)
    effect_forex_exchange = FloatField(default=0, blank=True, null=True)
    net_change_cash = FloatField(default=0, blank=True, null=True)
    cash_end_period = FloatField(default=0, blank=True, null=True)
    cash_beginning_period = FloatField(default=0, blank=True, null=True)
    operating_cf = FloatField(default=0, blank=True, null=True)
    capex = FloatField(default=0, blank=True, null=True)
    fcf = FloatField(default=0, blank=True, null=True)

    class Meta(BaseStatement.Meta):
        verbose_name = "Finprep Cash flow Statement"
        verbose_name_plural = "Finprep Cash flow Statements"
        db_table = "assets_companies_cashflow_statements_finprep"

    def __str__(self):
        return self.company.ticker + str(self.date)

    @property
    def cash_conversion_ratio_to_save(self):
        return self.fcf / self.net_income if self.net_income != 0 else 0
