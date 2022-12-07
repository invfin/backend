from typing import Union


from .utils import divide_or_zero, modify_for_percentage


class NonGaap:
    @classmethod
    def calculate_normalized_income(
        cls,
        net_income: Union[int, float],
        total_other_income_expenses_net: Union[int, float],
    )->Union[int, float]:
        return (
            net_income -
            total_other_income_expenses_net
        )

    @classmethod
    def calculate_effective_tax_rate(
        cls,
        income_tax_expense: Union[int, float],
        operating_income: Union[int, float],
    )->Union[int, float]:
        return divide_or_zero(
            income_tax_expense,
            operating_income,
        )

    @classmethod
    def calculate_net_working_cap(
        cls,
        total_current_assets: Union[int, float],
        total_current_liabilities: Union[int, float],
    )->Union[int, float]:
        return (
            total_current_assets -
            total_current_liabilities
        )

    @classmethod
    def calculate_average_inventory(
        cls,
        last_year_inventory: Union[int, float],
        inventory: Union[int, float],
    )->Union[int, float]:
        return round((
            last_year_inventory +
            inventory
        ) / 2, 2)

    @classmethod
    def calculate_average_payables(
        cls,
        last_year_accounts_payable: Union[int, float],
        accounts_payable: Union[int, float],
    )->Union[int, float]:
        return round((
                         last_year_accounts_payable +
                         accounts_payable
                     ) / 2, 2)

    @classmethod
    def calculate_divs_per_share(
        cls,
        dividends_paid: Union[int, float],
        common_stock: Union[int, float],
    )->Union[int, float]:
        return divide_or_zero(
            dividends_paid,
            common_stock,
        )

    @classmethod
    def calculate_dividend_yield(
        cls,
        divs_per_share: Union[int, float],
        current_price: Union[int, float],
    )->Union[int, float]:
        value = divide_or_zero(
            divs_per_share,
            current_price,
        )

        return modify_for_percentage(value)

    @classmethod
    def calculate_earnings_yield(
        cls,
        earnings_per_share: Union[int, float],
        current_price: Union[int, float],
    )->Union[int, float]:
        value = divide_or_zero(
            earnings_per_share,
            current_price,
        )
        return modify_for_percentage(value)

    @classmethod
    def calculate_fcf_yield(
        cls,
        free_cashflow_per_share: Union[int, float],
        current_price: Union[int, float],
    )->Union[int, float]:
        value = divide_or_zero(
            free_cashflow_per_share,
            current_price,
        )
        return modify_for_percentage(value)

    @classmethod
    def calculate_income_quality(
        cls,
        net_cash_provided_by_operating_activities: Union[int, float],
        net_income: Union[int, float],
    )->Union[int, float]:
        value = divide_or_zero(
            net_cash_provided_by_operating_activities,
            net_income,
        )
        return modify_for_percentage(value)

    @classmethod
    def calculate_invested_capital(
        cls,
        property_plant_equipment_net: Union[int, float],
        net_working_capital: Union[int, float],
        cash_and_cash_equivalents: Union[int, float],
    )->Union[int, float]:
        return (
            property_plant_equipment_net +
            net_working_capital -
            cash_and_cash_equivalents
        )

    @classmethod
    def calculate_market_cap(
        cls,
        current_price: Union[int, float],
        weighted_average_shares_out: Union[int, float],
    )->Union[int, float]:
        return divide_or_zero(
            current_price,
            weighted_average_shares_out,
        )

    @classmethod
    def calculate_net_current_asset_value(
        cls,
        total_current_assets: Union[int, float],
        total_liabilities: Union[int, float],
        weighted_average_shares_outstanding: Union[int, float],
    )->Union[int, float]:
        cash_available = total_current_assets - total_liabilities
        return divide_or_zero(
            cash_available,
            weighted_average_shares_outstanding,
        )

    @classmethod
    def calculate_payout_ratio(
        cls,
        dividends_paid: Union[int, float],
        net_income: Union[int, float],
    )->Union[int, float]:
        value = divide_or_zero(
            dividends_paid,
            net_income,
        )
        return modify_for_percentage(value)

    @classmethod
    def calculate_tangible_assets(
        cls,
        total_current_assets: Union[int, float],
        property_plant_equipment_net: Union[int, float],
    )->Union[int, float]:
        return (
            total_current_assets +
            property_plant_equipment_net
        )

    @classmethod
    def calculate_retention_ratio(
        cls,
        dividends_paid: Union[int, float],
        net_income: Union[int, float],
    )->Union[int, float]:
        value = divide_or_zero(
            (net_income - dividends_paid),
            net_income,
        )
        return modify_for_percentage(value)
