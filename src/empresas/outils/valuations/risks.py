def calculate_company_risk_score(risk_category_analyzers, company_ratios):
    weighted_scores = {}

    for category, analyzer in risk_category_analyzers.items():
        situation_scores = analyzer.calculate_situation_score(company_ratios[category])
        weighted_score = sum(
            score * weight
            for ratio_name, score, weight in zip(
                situation_scores.keys(), situation_scores.values(), analyzer.weights
            )
        )
        weighted_scores[category] = weighted_score

    return sum(
        weighted_scores[category] * weight
        for category, weight in overall_weight_per_category.items()
    )


class FinancialRatioAnalyzer:
    def __init__(
        self,
        ratio_fields,
        lower_thresholds,
        upper_thresholds,
        weight_lower=0.7,
        weight_upper=0.3,
    ):
        self.ratio_fields = ratio_fields
        self.lower_thresholds = lower_thresholds
        self.upper_thresholds = upper_thresholds
        self.weight_lower = weight_lower
        self.weight_upper = weight_upper

    def calculate_situation_score(self, company_ratios):
        overall_scores = {}

        for ratio_name in self.ratio_fields:
            ratio_value = getattr(company_ratios, ratio_name)
            lower_threshold = self.lower_thresholds[ratio_name]
            upper_threshold = self.upper_thresholds[ratio_name]

            max_possible_distance = max(
                upper_threshold - lower_threshold,
                ratio_value - lower_threshold,
                upper_threshold - ratio_value,
            )
            distance_to_lower = abs(ratio_value - lower_threshold)
            distance_to_upper = abs(ratio_value - upper_threshold)

            proximity_score_lower = 1 - (distance_to_lower / max_possible_distance)
            proximity_score_upper = 1 - (distance_to_upper / max_possible_distance)

            overall_situation_score = (self.weight_lower * proximity_score_lower) + (
                self.weight_upper * proximity_score_upper
            )

            overall_scores[ratio_name] = overall_situation_score

        return overall_scores


rentability_thresholds = {
    "roa": {
        "lower_threshold": 0.03,
        "upper_threshold": 0.10,
        "weight_lower": 0.6,
        "weight_upper": 0.4,
    },
    "roe": {
        "lower_threshold": 0.08,
        "upper_threshold": 0.20,
        "weight_lower": 0.7,
        "weight_upper": 0.3,
    },
    "roc": {
        "lower_threshold": 0.10,
        "upper_threshold": 0.25,
        "weight_lower": 0.6,
        "weight_upper": 0.4,
    },
    "roce": {
        "lower_threshold": 0.08,
        "upper_threshold": 0.18,
        "weight_lower": 0.7,
        "weight_upper": 0.3,
    },
    "rota": {
        "lower_threshold": 0.05,
        "upper_threshold": 0.15,
        "weight_lower": 0.6,
        "weight_upper": 0.4,
    },
    "roic": {
        "lower_threshold": 0.10,
        "upper_threshold": 0.25,
        "weight_lower": 0.6,
        "weight_upper": 0.4,
    },
    "nopat_roic": {
        "lower_threshold": 0.08,
        "upper_threshold": 0.20,
        "weight_lower": 0.7,
        "weight_upper": 0.3,
    },
    "rogic": {
        "lower_threshold": 0.12,
        "upper_threshold": 0.30,
        "weight_lower": 0.6,
        "weight_upper": 0.4,
    },
}

liquidity_thresholds = {
    "cash_ratio": {
        "lower_threshold": 0.10,
        "upper_threshold": 0.25,
        "weight_lower": 0.6,
        "weight_upper": 0.4,
    },
    "current_ratio": {
        "lower_threshold": 1.5,
        "upper_threshold": 3.0,
        "weight_lower": 0.7,
        "weight_upper": 0.3,
    },
    "quick_ratio": {
        "lower_threshold": 1.0,
        "upper_threshold": 2.0,
        "weight_lower": 0.7,
        "weight_upper": 0.3,
    },
    "operating_cashflow_ratio": {
        "lower_threshold": 0.10,
        "upper_threshold": 0.25,
        "weight_lower": 0.6,
        "weight_upper": 0.4,
    },
    "debt_to_equity": {
        "lower_threshold": 0.0,
        "upper_threshold": 1.0,
        "weight_lower": 0.7,
        "weight_upper": 0.3,
    },
}

margin_thresholds = {
    "gross_margin": {
        "lower_threshold": 0.30,
        "upper_threshold": 0.60,
        "weight_lower": 0.6,
        "weight_upper": 0.4,
    },
    "ebitda_margin": {
        "lower_threshold": 0.15,
        "upper_threshold": 0.30,
        "weight_lower": 0.7,
        "weight_upper": 0.3,
    },
    "net_income_margin": {
        "lower_threshold": 0.10,
        "upper_threshold": 0.25,
        "weight_lower": 0.7,
        "weight_upper": 0.3,
    },
    "fcf_margin": {
        "lower_threshold": 0.08,
        "upper_threshold": 0.20,
        "weight_lower": 0.6,
        "weight_upper": 0.4,
    },
    "fcf_equity_to_net_income": {
        "lower_threshold": 0.15,
        "upper_threshold": 0.35,
        "weight_lower": 0.7,
        "weight_upper": 0.3,
    },
    "unlevered_fcf_to_net_income": {
        "lower_threshold": 0.10,
        "upper_threshold": 0.25,
        "weight_lower": 0.6,
        "weight_upper": 0.4,
    },
    "unlevered_fcf_ebit_to_net_income": {
        "lower_threshold": 0.10,
        "upper_threshold": 0.25,
        "weight_lower": 0.7,
        "weight_upper": 0.3,
    },
    "owners_earnings_to_net_income": {
        "lower_threshold": 0.10,
        "upper_threshold": 0.25,
        "weight_lower": 0.6,
        "weight_upper": 0.4,
    },
}

per_share_value_thresholds = {
    "sales_ps": {
        "lower_threshold": 0.5,
        "upper_threshold": 2.0,
        "weight_lower": 0.7,
        "weight_upper": 0.3,
    },
    "book_ps": {
        "lower_threshold": 0.8,
        "upper_threshold": 2.5,
        "weight_lower": 0.6,
        "weight_upper": 0.4,
    },
    "tangible_ps": {
        "lower_threshold": 0.7,
        "upper_threshold": 2.0,
        "weight_lower": 0.7,
        "weight_upper": 0.3,
    },
    "fcf_ps": {
        "lower_threshold": 0.5,
        "upper_threshold": 1.5,
        "weight_lower": 0.6,
        "weight_upper": 0.4,
    },
    "eps": {
        "lower_threshold": 0.8,
        "upper_threshold": 2.0,
        "weight_lower": 0.7,
        "weight_upper": 0.3,
    },
    "cash_ps": {
        "lower_threshold": 0.3,
        "upper_threshold": 1.5,
        "weight_lower": 0.7,
        "weight_upper": 0.3,
    },
    "operating_cf_ps": {
        "lower_threshold": 0.5,
        "upper_threshold": 2.0,
        "weight_lower": 0.6,
        "weight_upper": 0.4,
    },
    "capex_ps": {
        "lower_threshold": 0.2,
        "upper_threshold": 1.0,
        "weight_lower": 0.7,
        "weight_upper": 0.3,
    },
    "total_assets_ps": {
        "lower_threshold": 0.8,
        "upper_threshold": 2.5,
        "weight_lower": 0.6,
        "weight_upper": 0.4,
    },
}

operation_risk_thresholds = {
    "asset_coverage_ratio": {
        "lower_threshold": 1.5,
        "upper_threshold": 3.0,
        "weight_lower": 0.7,
        "weight_upper": 0.3,
    },
    "cash_flow_coverage_ratios": {
        "lower_threshold": 1.2,
        "upper_threshold": 2.5,
        "weight_lower": 0.6,
        "weight_upper": 0.4,
    },
    "cash_coverage": {
        "lower_threshold": 0.15,
        "upper_threshold": 0.30,
        "weight_lower": 0.7,
        "weight_upper": 0.3,
    },
    "debt_service_coverage": {
        "lower_threshold": 1.5,
        "upper_threshold": 3.0,
        "weight_lower": 0.6,
        "weight_upper": 0.4,
    },
    "interest_coverage": {
        "lower_threshold": 3.0,
        "upper_threshold": 6.0,
        "weight_lower": 0.7,
        "weight_upper": 0.3,
    },
    "operating_cashflow_ratio": {
        "lower_threshold": 0.15,
        "upper_threshold": 0.30,
        "weight_lower": 0.6,
        "weight_upper": 0.4,
    },
    "debt_ratio": {
        "lower_threshold": 0.0,
        "upper_threshold": 0.5,
        "weight_lower": 0.7,
        "weight_upper": 0.3,
    },
    "long_term_debt_to_capitalization": {
        "lower_threshold": 0.0,
        "upper_threshold": 0.4,
        "weight_lower": 0.6,
        "weight_upper": 0.4,
    },
    "total_debt_to_capitalization": {
        "lower_threshold": 0.0,
        "upper_threshold": 0.5,
        "weight_lower": 0.7,
        "weight_upper": 0.3,
    },
}

enterprise_value_thresholds = {
    "ev_fcf": {
        "lower_threshold": 10.0,
        "upper_threshold": 20.0,
        "weight_lower": 0.7,
        "weight_upper": 0.3,
    },
    "ev_operating_cf": {
        "lower_threshold": 10.0,
        "upper_threshold": 20.0,
        "weight_lower": 0.6,
        "weight_upper": 0.4,
    },
    "ev_sales": {
        "lower_threshold": 1.0,
        "upper_threshold": 2.5,
        "weight_lower": 0.7,
        "weight_upper": 0.3,
    },
    "company_equity_multiplier": {
        "lower_threshold": 1.0,
        "upper_threshold": 2.5,
        "weight_lower": 0.6,
        "weight_upper": 0.4,
    },
    "ev_multiple": {
        "lower_threshold": 10.0,
        "upper_threshold": 20.0,
        "weight_lower": 0.7,
        "weight_upper": 0.3,
    },
}

company_growth_thresholds = {
    "revenue_growth": {
        "lower_threshold": 0.05,
        "upper_threshold": 0.15,
        "weight_lower": 0.6,
        "weight_upper": 0.4,
    },
    "cost_revenue_growth": {
        "lower_threshold": -0.05,
        "upper_threshold": 0.05,
        "weight_lower": 0.7,
        "weight_upper": 0.3,
    },
    "operating_expenses_growth": {
        "lower_threshold": 0.0,
        "upper_threshold": 0.10,
        "weight_lower": 0.7,
        "weight_upper": 0.3,
    },
    "net_income_growth": {
        "lower_threshold": 0.05,
        "upper_threshold": 0.15,
        "weight_lower": 0.6,
        "weight_upper": 0.4,
    },
    "shares_buyback": {
        "lower_threshold": -0.02,
        "upper_threshold": 0.02,
        "weight_lower": 0.7,
        "weight_upper": 0.3,
    },
    "eps_growth": {
        "lower_threshold": 0.05,
        "upper_threshold": 0.15,
        "weight_lower": 0.6,
        "weight_upper": 0.4,
    },
    "fcf_growth": {
        "lower_threshold": 0.05,
        "upper_threshold": 0.15,
        "weight_lower": 0.7,
        "weight_upper": 0.3,
    },
    "owners_earnings_growth": {
        "lower_threshold": 0.05,
        "upper_threshold": 0.15,
        "weight_lower": 0.6,
        "weight_upper": 0.4,
    },
    "capex_growth": {
        "lower_threshold": -0.05,
        "upper_threshold": 0.05,
        "weight_lower": 0.7,
        "weight_upper": 0.3,
    },
    "rd_expenses_growth": {
        "lower_threshold": 0.0,
        "upper_threshold": 0.10,
        "weight_lower": 0.6,
        "weight_upper": 0.4,
    },
}

efficiency_thresholds = {
    "asset_turnover": {
        "lower_threshold": 0.5,
        "upper_threshold": 1.5,
        "weight_lower": 0.7,
        "weight_upper": 0.3,
    },
    "inventory_turnover": {
        "lower_threshold": 5.0,
        "upper_threshold": 12.0,
        "weight_lower": 0.6,
        "weight_upper": 0.4,
    },
    "fixed_asset_turnover": {
        "lower_threshold": 2.0,
        "upper_threshold": 6.0,
        "weight_lower": 0.7,
        "weight_upper": 0.3,
    },
    "accounts_payable_turnover": {
        "lower_threshold": 6.0,
        "upper_threshold": 15.0,
        "weight_lower": 0.6,
        "weight_upper": 0.4,
    },
    "cash_conversion_cycle": {
        "lower_threshold": -30.0,
        "upper_threshold": 30.0,
        "weight_lower": 0.7,
        "weight_upper": 0.3,
    },
    "days_inventory_outstanding": {
        "lower_threshold": 20.0,
        "upper_threshold": 60.0,
        "weight_lower": 0.6,
        "weight_upper": 0.4,
    },
    "days_payables_outstanding": {
        "lower_threshold": 30.0,
        "upper_threshold": 60.0,
        "weight_lower": 0.7,
        "weight_upper": 0.3,
    },
    "days_sales_outstanding": {
        "lower_threshold": 20.0,
        "upper_threshold": 45.0,
        "weight_lower": 0.6,
        "weight_upper": 0.4,
    },
    "free_cashflow_to_operating_cashflow": {
        "lower_threshold": 0.8,
        "upper_threshold": 1.2,
        "weight_lower": 0.7,
        "weight_upper": 0.3,
    },
    "operating_cycle": {
        "lower_threshold": 40.0,
        "upper_threshold": 90.0,
        "weight_lower": 0.6,
        "weight_upper": 0.4,
    },
    "cash_conversion_ratio": {
        "lower_threshold": -0.2,
        "upper_threshold": 0.2,
        "weight_lower": 0.7,
        "weight_upper": 0.3,
    },
}

price_to_ratio_thresholds = {
    "price_book": {
        "lower_threshold": 1.0,
        "upper_threshold": 3.0,
        "weight_lower": 0.6,
        "weight_upper": 0.4,
    },
    "price_cf": {
        "lower_threshold": 10.0,
        "upper_threshold": 20.0,
        "weight_lower": 0.7,
        "weight_upper": 0.3,
    },
    "price_earnings": {
        "lower_threshold": 10.0,
        "upper_threshold": 20.0,
        "weight_lower": 0.7,
        "weight_upper": 0.3,
    },
    "price_earnings_growth": {
        "lower_threshold": 0.5,
        "upper_threshold": 2.0,
        "weight_lower": 0.6,
        "weight_upper": 0.4,
    },
    "price_sales": {
        "lower_threshold": 1.0,
        "upper_threshold": 3.0,
        "weight_lower": 0.7,
        "weight_upper": 0.3,
    },
    "price_total_assets": {
        "lower_threshold": 0.5,
        "upper_threshold": 1.5,
        "weight_lower": 0.6,
        "weight_upper": 0.4,
    },
    "price_fcf": {
        "lower_threshold": 10.0,
        "upper_threshold": 25.0,
        "weight_lower": 0.7,
        "weight_upper": 0.3,
    },
    "price_operating_cf": {
        "lower_threshold": 10.0,
        "upper_threshold": 25.0,
        "weight_lower": 0.6,
        "weight_upper": 0.4,
    },
    "price_tangible_assets": {
        "lower_threshold": 0.5,
        "upper_threshold": 2.0,
        "weight_lower": 0.7,
        "weight_upper": 0.3,
    },
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
