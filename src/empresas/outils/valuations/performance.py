from typing import Dict, List, Union


def calculate_altman_z_score(ratios):
    # Define the coefficients for the Altman Z-Score formula
    coefficients = {
        "working_capital_ratio": 1.2,
        "retained_earnings_to_total_assets": 1.4,
        "ebit_to_total_assets": 3.3,
        "market_value_of_equity_to_book_value_of_total_liabilities": 0.6,
        "sales_to_total_assets": 1.0,
    }

    return (
        coefficients["working_capital_ratio"] * ratios["working_capital_ratio"]
        + coefficients["retained_earnings_to_total_assets"]
        * ratios["retained_earnings_to_total_assets"]
        + coefficients["ebit_to_total_assets"] * ratios["ebit_to_total_assets"]
        + coefficients["market_value_of_equity_to_book_value_of_total_liabilities"]
        * ratios["market_value_of_equity_to_book_value_of_total_liabilities"]
        + coefficients["sales_to_total_assets"] * ratios["sales_to_total_assets"]
    )


def calculate_beneish_m_score(ratios):
    # Define the coefficients for the Beneish M-Score formula
    coefficients = {
        "dsri": -4.84,
        "gm": 0.92,
        "aqi": 0.528,
        "sgi": 6.01,
        "dep": -1.03,
        "sgi_aqi": -0.172,
        "accruals": -1.73,
        "leverage": -2.37,
        "tata": -1.73,
    }

    return (
        coefficients["dsri"] * ratios["dsri"]
        + coefficients["gm"] * ratios["gm"]
        + coefficients["aqi"] * ratios["aqi"]
        + coefficients["sgi"] * ratios["sgi"]
        + coefficients["dep"] * ratios["dep"]
        + coefficients["sgi_aqi"] * ratios["sgi_aqi"]
        + coefficients["accruals"] * ratios["accruals"]
        + coefficients["leverage"] * ratios["leverage"]
        + coefficients["tata"] * ratios["tata"]
    )


def calculate_piotroski_f_score(ratios):
    # Define the Piotroski criteria with their corresponding ratios
    criteria = {
        "positive_net_income": ratios["net_income_growth"] > 0,
        "positive_operating_cashflow": ratios["operating_cashflow_ratio"] > 0,
        "roa_positive": ratios["roa"] > 0,
        "positive_cash_flow": ratios["cash_flow_coverage_ratios"] > 0,
        "decreasing_long_term_debt": (
            ratios["long_term_debt_to_capitalization"]
            < ratios["long_term_debt_to_capitalization"]
        ),
        "increasing_current_ratio": ratios["current_ratio"] > ratios["current_ratio"],
        "no_dilution": ratios["shares_buyback"] > 0 or ratios["eps_growth"] > 0,
        "increasing_roa": ratios["roa"] > ratios["roa"],
        "increasing_roe": ratios["roe"] > ratios["roe"],
    }

    return sum(criteria.values())


def calculate_ratio_performance(
    values: List[Union[int, float]],
    weights: Dict[str, Union[int, float]],
) -> float:
    return _normalized_weighted_average(_normalize_values(values), weights)


def _normalize_values(values: List[Union[int, float]]):
    # Perform min-max scaling to normalize ratio between 0 and 1
    min_val = min(values)
    max_val = max(values)
    return [(x - min_val) / (max_val - min_val) for x in values]


def _normalized_weighted_average(
    normalized_values: List[Union[int, float]],
    weights: Dict[str, Union[int, float]],
) -> float:
    # Calculate the weighted average of normalized ratios
    return sum(w * r for w, r in zip(weights, normalized_values))


rentability_weights = {
    "roa": 0.1,
    "roe": 0.15,
    "roc": 0.1,
    "roce": 0.15,
    "rota": 0.1,
    "roic": 0.15,
    "nopat_roic": 0.1,
    "rogic": 0.05,
}

liquidity_weights = {
    "cash_ratio": 0.1,
    "current_ratio": 0.15,
    "quick_ratio": 0.15,
    "operating_cashflow_ratio": 0.2,
    "debt_to_equity": 0.4,
}

margin_weights = {
    "gross_margin": 0.15,
    "ebitda_margin": 0.15,
    "net_income_margin": 0.2,
    "fcf_margin": 0.2,
    "fcf_equity_to_net_income": 0.1,
    "unlevered_fcf_to_net_income": 0.05,
    "unlevered_fcf_ebit_to_net_income": 0.05,
    "owners_earnings_to_net_income": 0.1,
}

per_share_value_weights = {
    "sales_ps": 0.1,
    "book_ps": 0.15,
    "tangible_ps": 0.1,
    "fcf_ps": 0.15,
    "eps": 0.2,
    "cash_ps": 0.05,
    "operating_cf_ps": 0.05,
    "capex_ps": 0.05,
    "total_assets_ps": 0.05,
}

operation_risk_weights = {
    "asset_coverage_ratio": 0.15,
    "cash_flow_coverage_ratios": 0.1,
    "cash_coverage": 0.1,
    "debt_service_coverage": 0.1,
    "interest_coverage": 0.1,
    "operating_cashflow_ratio": 0.15,
    "debt_ratio": 0.1,
    "long_term_debt_to_capitalization": 0.05,
    "total_debt_to_capitalization": 0.05,
}

ev_ratio_weights = {
    "market_cap": 0.15,
    "enterprise_value": 0.15,
    "ev_fcf": 0.2,
    "ev_operating_cf": 0.15,
    "ev_sales": 0.15,
    "company_equity_multiplier": 0.05,
    "ev_multiple": 0.1,
}

growth_weights = {
    "revenue_growth": 0.15,
    "cost_revenue_growth": 0.1,
    "operating_expenses_growth": 0.1,
    "net_income_growth": 0.15,
    "shares_buyback": 0.05,
    "eps_growth": 0.1,
    "fcf_growth": 0.1,
    "owners_earnings_growth": 0.05,
    "capex_growth": 0.05,
    "rd_expenses_growth": 0.05,
}

efficiency_weights = {
    "asset_turnover": 0.1,
    "inventory_turnover": 0.1,
    "fixed_asset_turnover": 0.1,
    "accounts_payable_turnover": 0.1,
    "cash_conversion_cycle": 0.15,
    "days_inventory_outstanding": 0.1,
    "days_payables_outstanding": 0.1,
    "days_sales_outstanding": 0.1,
    "free_cashflow_to_operating_cashflow": 0.1,
    "operating_cycle": 0.1,
    "cash_conversion_ratio": 0.05,
}

price_to_weights = {
    "price_book": 0.15,
    "price_cf": 0.15,
    "price_earnings": 0.2,
    "price_earnings_growth": 0.15,
    "price_sales": 0.1,
    "price_total_assets": 0.05,
    "price_fcf": 0.1,
    "price_operating_cf": 0.1,
    "price_tangible_assets": 0.05,
}

overall_weight_per_category = {
    "rentability_ratios": 0.2,
    "liquidity_ratios": 0.15,
    "margin_ratios": 0.15,
    "per_share_value_ratios": 0.1,
    "operation_risk_ratios": 0.1,
    "enterprise_value_ratios": 0.1,
    "growth_rates": 0.05,
    "efficiency_ratios": 0.05,
    "price_to_ratios": 0.1,
}
