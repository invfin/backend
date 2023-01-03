from django.db import QuerySet


class StatementQuerySet(QuerySet):
    def average_margins(self):
        return

    def average_efficiency_ratios(self):
        return

    def average_growth_rates(self):
        return

    def average_per_share_values(self):
        return

    def average_price_to_ratios(self):
        return

    def average_liquidity_ratios(self):
        return

    def average_rentability_ratios(self):
        return

    def average_operation_risks_ratios(self):
        # Operation risk
        return all_operation_risks_ratios.aggregate(
            average_asset_coverage_ratio=Avg("asset_coverage_ratio"),
            average_cash_flow_coverage_ratios = Avg("cash_flow_coverage_ratios"),
            average_cash_coverage = Avg("cash_coverage"),
            average_debt_service_coverage = Avg("debt_service_coverage"),
            average_interest_coverage = Avg("interest_coverage"),
            average_operating_cashflow_ratio = Avg("operating_cashflow_ratio"),
            average_debt_ratio = Avg("debt_ratio"),
            average_long_term_debt_to_capitalization = Avg("long_term_debt_to_capitalization"),
            average_total_debt_to_capitalization = Avg("total_debt_to_capitalization"),
        )

    def average_ev_ratios(self):
        return


    def calculate_averages(
        self,
        all_margins: list = None,
        all_efficiency_ratios: list = None,
        all_growth_rates: list = None,
        all_per_share_values: list = None,
        all_price_to_ratios: list = None,
        all_liquidity_ratios: list = None,
        all_rentability_ratios: list = None,
        all_operation_risks_ratios: list = None,
        all_ev_ratios: list = None,
    ) -> dict:
        # TODO fix averages
        return {}


        # Per share
        average_sales_ps = all_per_share_values.aggregate(average_sales_ps=Avg("sales_ps"))
        average_book_ps = all_per_share_values.aggregate(average_book_ps=Avg("book_ps"))
        average_tangible_ps = all_per_share_values.aggregate(average_tangible_ps=Avg("tangible_ps"))
        average_fcf_ps = all_per_share_values.aggregate(average_fcf_ps=Avg("fcf_ps"))
        average_eps = all_per_share_values.aggregate(average_eps=Avg("eps"))
        average_cash_ps = all_per_share_values.aggregate(average_cash_ps=Avg("cash_ps"))
        average_operating_cf_ps = all_per_share_values.aggregate(average_operating_cf_ps=Avg("operating_cf_ps"))
        average_capex_ps = all_per_share_values.aggregate(average_capex_ps=Avg("capex_ps"))
        average_total_assets_ps = all_per_share_values.aggregate(average_total_assets_ps=Avg("total_assets_ps"))
        # Price to
        average_price_book = all_price_to_ratios.aggregate(average_price_book=Avg("price_book"))
        average_price_cf = all_price_to_ratios.aggregate(average_price_cf=Avg("price_cf"))
        average_price_earnings = all_price_to_ratios.aggregate(average_price_earnings=Avg("price_earnings"))
        average_price_earnings_growth = all_price_to_ratios.aggregate(
            average_price_earnings_growth=Avg("price_earnings_growth")
        )
        average_price_sales = all_price_to_ratios.aggregate(average_price_sales=Avg("price_sales"))
        average_price_total_assets = all_price_to_ratios.aggregate(average_price_total_assets=Avg("price_total_assets"))
        average_price_fcf = all_price_to_ratios.aggregate(average_price_fcf=Avg("price_fcf"))
        average_price_operating_cf = all_price_to_ratios.aggregate(average_price_operating_cf=Avg("price_operating_cf"))
        average_price_tangible_assets = all_price_to_ratios.aggregate(
            average_price_tangible_assets=Avg("price_tangible_assets")
        )
        # Efficiency
        average_asset_turnover = all_efficiency_ratios.aggregate(average_asset_turnover=Avg("asset_turnover"))
        average_inventory_turnover = all_efficiency_ratios.aggregate(
            average_inventory_turnover=Avg("inventory_turnover")
        )
        average_fixed_asset_turnover = all_efficiency_ratios.aggregate(
            average_fixed_asset_turnover=Avg("fixed_asset_turnover")
        )
        average_accounts_payable_turnover = all_efficiency_ratios.aggregate(
            average_accounts_payable_turnover=Avg("accounts_payable_turnover")
        )
        average_cash_conversion_cycle = all_efficiency_ratios.aggregate(
            average_cash_conversion_cycle=Avg("cash_conversion_cycle")
        )
        average_days_inventory_outstanding = all_efficiency_ratios.aggregate(
            average_days_inventory_outstanding=Avg("days_inventory_outstanding")
        )
        average_days_payables_outstanding = all_efficiency_ratios.aggregate(
            average_days_payables_outstanding=Avg("days_payables_outstanding")
        )
        average_days_sales_outstanding = all_efficiency_ratios.aggregate(
            average_days_sales_outstanding=Avg("days_sales_outstanding")
        )
        average_free_cashflow_to_operating_cashflow = all_efficiency_ratios.aggregate(
            average_free_cashflow_to_operating_cashflow=Avg("free_cashflow_to_operating_cashflow")
        )
        average_operating_cycle = all_efficiency_ratios.aggregate(average_operating_cycle=Avg("operating_cycle"))
        # Growth
        average_revenue_growth = all_growth_rates.aggregate(average_revenue_growth=Avg("revenue_growth"))
        average_cost_revenue_growth = all_growth_rates.aggregate(average_cost_revenue_growth=Avg("cost_revenue_growth"))
        average_operating_expenses_growth = all_growth_rates.aggregate(
            average_operating_expenses_growth=Avg("operating_expenses_growth")
        )
        average_net_income_growth = all_growth_rates.aggregate(average_net_income_growth=Avg("net_income_growth"))
        average_shares_buyback = all_growth_rates.aggregate(average_shares_buyback=Avg("shares_buyback"))
        average_eps_growth = all_growth_rates.aggregate(average_eps_growth=Avg("eps_growth"))
        average_fcf_growth = all_growth_rates.aggregate(average_fcf_growth=Avg("fcf_growth"))
        average_owners_earnings_growth = all_growth_rates.aggregate(
            average_owners_earnings_growth=Avg("owners_earnings_growth")
        )
        average_capex_growth = all_growth_rates.aggregate(average_capex_growth=Avg("capex_growth"))
        average_rd_expenses_growth = all_growth_rates.aggregate(average_rd_expenses_growth=Avg("rd_expenses_growth"))
        # Margins
        average_gross_margin = all_margins.aggregate(average_gross_margin=Avg("gross_margin"))
        average_ebitda_margin = all_margins.aggregate(average_ebitda_margin=Avg("ebitda_margin"))
        average_net_income_margin = all_margins.aggregate(average_net_income_margin=Avg("net_income_margin"))
        average_fcf_margin = all_margins.aggregate(average_fcf_margin=Avg("fcf_margin"))
        average_fcf_equity_to_net_income = all_margins.aggregate(
            average_fcf_equity_to_net_income=Avg("fcf_equity_to_net_income")
        )
        average_unlevered_fcf_to_net_income = all_margins.aggregate(
            average_unlevered_fcf_to_net_income=Avg("unlevered_fcf_to_net_income")
        )
        average_unlevered_fcf_ebit_to_net_income = all_margins.aggregate(
            average_unlevered_fcf_ebit_to_net_income=Avg("unlevered_fcf_ebit_to_net_income")
        )
        average_owners_earnings_to_net_income = all_margins.aggregate(
            average_owners_earnings_to_net_income=Avg("owners_earnings_to_net_income")
        )
        # Rentability
        average_roa = all_rentability_ratios.aggregate(average_roa=Avg("roa"))
        average_roe = all_rentability_ratios.aggregate(average_roe=Avg("roe"))
        average_roc = all_rentability_ratios.aggregate(average_roc=Avg("roc"))
        average_roce = all_rentability_ratios.aggregate(average_roce=Avg("roce"))
        average_rota = all_rentability_ratios.aggregate(average_rota=Avg("rota"))
        average_roic = all_rentability_ratios.aggregate(average_roic=Avg("roic"))
        average_nopat_roic = all_rentability_ratios.aggregate(average_nopat_roic=Avg("nopat_roic"))
        average_rogic = all_rentability_ratios.aggregate(average_rogic=Avg("rogic"))
        # Liquidity
        average_cash_ratio = all_liquidity_ratios.aggregate(average_cash_ratio=Avg("cash_ratio"))
        average_current_ratio = all_liquidity_ratios.aggregate(average_current_ratio=Avg("current_ratio"))
        average_quick_ratio = all_liquidity_ratios.aggregate(average_quick_ratio=Avg("quick_ratio"))
        average_operating_cashflow_ratio = all_liquidity_ratios.aggregate(
            average_operating_cashflow_ratio=Avg("operating_cashflow_ratio")
        )
        average_debt_to_equity = all_liquidity_ratios.aggregate(average_debt_to_equity=Avg("debt_to_equity"))
        # Enterprise value
        average_ev_fcf = all_ev_ratios.aggregate(average_ev_fcf=Avg("ev_fcf"))
        average_ev_operating_cf = all_ev_ratios.aggregate(average_ev_operating_cf=Avg("ev_operating_cf"))
        average_ev_sales = all_ev_ratios.aggregate(average_ev_sales=Avg("ev_sales"))
        average_company_equity_multiplier = all_ev_ratios.aggregate(
            average_company_equity_multiplier=Avg("company_equity_multiplier")
        )
        average_ev_multiple = all_ev_ratios.aggregate(average_ev_multiple=Avg("ev_multiple"))

        return {
            **average_sales_ps,
            **average_book_ps,
            **average_tangible_ps,
            **average_fcf_ps,
            **average_eps,
            **average_cash_ps,
            **average_operating_cf_ps,
            **average_capex_ps,
            **average_total_assets_ps,
            **average_price_book,
            **average_price_cf,
            **average_price_earnings,
            **average_price_earnings_growth,
            **average_price_sales,
            **average_price_total_assets,
            **average_price_fcf,
            **average_price_operating_cf,
            **average_price_tangible_assets,
            **average_asset_turnover,
            **average_inventory_turnover,
            **average_fixed_asset_turnover,
            **average_accounts_payable_turnover,
            **average_cash_conversion_cycle,
            **average_days_inventory_outstanding,
            **average_days_payables_outstanding,
            **average_days_sales_outstanding,
            **average_free_cashflow_to_operating_cashflow,
            **average_operating_cycle,
            **average_revenue_growth,
            **average_cost_revenue_growth,
            **average_operating_expenses_growth,
            **average_net_income_growth,
            **average_shares_buyback,
            **average_eps_growth,
            **average_fcf_growth,
            **average_owners_earnings_growth,
            **average_capex_growth,
            **average_rd_expenses_growth,
            **average_gross_margin,
            **average_ebitda_margin,
            **average_net_income_margin,
            **average_fcf_margin,
            **average_fcf_equity_to_net_income,
            **average_unlevered_fcf_to_net_income,
            **average_unlevered_fcf_ebit_to_net_income,
            **average_owners_earnings_to_net_income,
            **average_roa,
            **average_roe,
            **average_roc,
            **average_roce,
            **average_rota,
            **average_roic,
            **average_nopat_roic,
            **average_rogic,
            **average_cash_ratio,
            **average_current_ratio,
            **average_quick_ratio,
            **average_operating_cashflow_ratio,
            **average_debt_to_equity,
            **average_asset_coverage_ratio,
            **average_cash_flow_coverage_ratios,
            **average_cash_coverage,
            **average_debt_service_coverage,
            **average_interest_coverage,
            **average_operating_cashflow_ratio,
            **average_debt_ratio,
            **average_long_term_debt_to_capitalization,
            **average_total_debt_to_capitalization,
            **average_ev_fcf,
            **average_ev_operating_cf,
            **average_ev_sales,
            **average_company_equity_multiplier,
            **average_ev_multiple,
        }
