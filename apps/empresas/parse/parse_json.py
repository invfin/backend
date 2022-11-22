import os, json, re, concurrent.futures, datetime, timeit, random

from tqdm import tqdm

from django.template.defaultfilters import slugify

from apps.empresas.models import (
    Company,
    IncomeStatementAsReported,
    BalanceSheetAsReported,
    CashflowStatementAsReported,
    StatementItemConcept,
    StatementItem,
)
from apps.periods.models import Period
from apps.currencies.models import Currency
from apps.periods import constants


pattern = re.compile(r"(?<!^)(?=[A-Z])")

MAIN_URL = "/home/lucas/Downloads/kaggle-companies-data"

income_fields = [
                "revenue_field",
                "cost_of_revenue_field",
                "gross_profit_field",
                "rd_expenses_field",
                "general_administrative_expenses_field",
                "selling_marketing_expenses_field",
                "sga_expenses_field",
                "other_expenses_field",
                "operating_expenses_field",
                "cost_and_expenses_field",
                "interest_expense_field",
                "depreciation_amortization_field",
                "ebitda_field",
                "operating_income_field",
                "net_total_other_income_expenses_field",
                "income_before_tax_field",
                "income_tax_expenses_field",
                "net_income_field",
                "weighted_average_shares_outstanding_field",
                "weighted_average_diluated_shares_outstanding_field",
            ]

balance_sheet_fields = ['cash_and_cash_equivalents_field', 'short_term_investments_field', 'cash_and_short_term_investments_field', 'net_receivables_field', 'inventory_field', 'other_current_assets_field', 'total_current_assets_field', 'property_plant_equipment_field', 'goodwill_field', 'intangible_assets_field', 'goodwill_and_intangible_assets_field', 'long_term_investments_field', 'tax_assets_field', 'other_non_current_assets_field', 'total_non_current_assets_field', 'other_assets_field', 'total_assets_field', 'account_payables_field', 'short_term_debt_field', 'tax_payables_field', 'deferred_revenue_field', 'other_current_liabilities_field', 'total_current_liabilities_field', 'long_term_debt_field', 'deferred_revenue_non_current_field', 'deferred_tax_liabilities_non_current_field', 'other_non_current_liabilities_field', 'total_non_current_liabilities_field', 'other_liabilities_field', 'total_liabilities_field', 'common_stocks_field', 'retained_earnings_field', 'accumulated_other_comprehensive_income_loss_field', 'othertotal_stockholders_equity_field', 'total_stockholders_equity_field', 'total_liabilities_and_total_equity_field', 'total_investments_field', 'total_debt_field', 'net_debt_field',]

cashflow_fields = ['net_income_field', 'depreciation_amortization_field', 'deferred_income_tax_field', 'stock_based_compesation_field', 'change_in_working_capital_field', 'accounts_receivables_field', 'inventory_field', 'accounts_payable_field', 'other_working_capital_field', 'other_non_cash_items_field', 'operating_activities_cf_field', 'investments_property_plant_equipment_field', 'acquisitions_net_field', 'purchases_investments_field', 'sales_maturities_investments_field', 'other_investing_activites_field', 'investing_activities_cf_field', 'debt_repayment_field', 'common_stock_issued_field', 'common_stock_repurchased_field', 'dividends_paid_field', 'other_financing_activities_field', 'financing_activities_cf_field', 'effect_forex_exchange_field', 'net_change_cash_field', 'cash_end_period_field', 'cash_beginning_period_field', 'operating_cf_field', 'capex_field', 'fcf_field',]


def camel_to_snake(word):
    return pattern.sub("_", word).lower().replace(":", "")


def snake_label(label: str):
    label = slugify(label)
    label = label.replace("-", "_")
    return label


def save_item_concept(concept, label, company) -> StatementItemConcept:
    concept_slug = camel_to_snake(concept)
    label_slug = snake_label(label)
    try:
        item_concept = StatementItemConcept.objects.get(
            concept=concept,
            label=label,
            label_slug=label_slug,
            concept_slug=concept_slug,
        )
    except StatementItemConcept.DoesNotExist:
        if concept.startswith(company.ticker.lower()):
            item_concept = StatementItemConcept.objects.create(
                concept=concept,
                label=label,
                concept_slug=concept_slug,
                label_slug=label_slug,
                company=company,
            )
        else:
            item_concept = StatementItemConcept.objects.create(
                concept=concept,
                label=label,
                concept_slug=concept_slug,
                label_slug=label_slug,
            )
    return item_concept


def retrieve_item(info, currency, company):
    currency_str = info["unit"]
    if currency_str == "shares" or currency_str == "usd/shares":
        use_currency = True
    else:
        use_currency = False
    currency = currency if use_currency else None
    value = info["value"]
    try:
        value = float(value)
    except ValueError:
        value = 0
    concept = save_item_concept(info["concept"], info["label"], company)
    return StatementItem.objects.create(concept=concept, value=value, unit=currency_str, currency=currency)


def save_lists(data, company, period, start_date, end_date, file, folder):
    cashflow = data["cf"]
    balance = data["bs"]
    income = data["ic"]
    currency = None
    items_inc = []
    items_bs = []
    items_cf = []
    for info_inc, info_bs, info_cf in zip(income, balance, cashflow):
        currency_str = info_inc["unit"]
        if not currency:
            if currency_str == "shares" or currency_str == "usd/shares":
                pass
            else:
                if currency_str == "usd":
                    currency = Currency.objects.get(currency=currency_str.upper(), symbol="$")
                else:
                    try:
                        currency, _ = Currency.objects.get_or_create(currency=currency_str.upper())
                    except Currency.MultipleObjectsReturned:
                        currency = Currency.objects.filter(currency=currency_str.upper()).first()

        items_inc.append(retrieve_item(info_inc, currency, company))
        items_bs.append(retrieve_item(info_bs, currency, company))
        items_cf.append(retrieve_item(info_cf, currency, company))

    data_shared_dict = dict(
        company=company,
        period=period,
        date=period.year,
        reported_currency=currency,
        start_date=start_date,
        end_date=end_date,
        from_file=file,
        from_folder=folder,
    )

    inc_st = IncomeStatementAsReported.objects.create(financial_data=income, **data_shared_dict)
    inc_st.fields.add(*items_inc)
    bs_st = BalanceSheetAsReported.objects.create(financial_data=balance, **data_shared_dict)
    bs_st.fields.add(*items_bs)
    cf_st = CashflowStatementAsReported.objects.create(financial_data=cashflow, **data_shared_dict)
    cf_st.fields.add(*items_cf)


def get_period(quarter):
    if quarter == "Q1":
        period = constants.PERIOD_1_QUARTER
    elif quarter == "Q2":
        period = constants.PERIOD_2_QUARTER
    elif quarter == "Q3":
        period = constants.PERIOD_3_QUARTER
    else:
        period = constants.PERIOD_FOR_YEAR
    return period


def parse_json(principal_data, file, folder):
    year = int(principal_data["year"])
    start_date = datetime.datetime.strptime(principal_data["startDate"], "%Y-%m-%d").date()
    end_date = datetime.datetime.strptime(principal_data["endDate"], "%Y-%m-%d").date()
    data = principal_data["data"]
    company, period_obj = None, None
    company, created = Company.objects.get_or_create(
        ticker=principal_data["symbol"], defaults={"name": "From-as-reported"}
    )
    period = get_period(principal_data["quarter"])
    period_obj = Period.objects.get(year=year, period=period)

    save_lists(data, company, period_obj, start_date, end_date, file, folder)


def save_json_content(file, folder):
    # we open the json and access to the data
    json_info_file = f"{MAIN_URL}/{folder}/{file}"
    with concurrent.futures.ThreadPoolExecutor() as executor:
        with open(f"{json_info_file}", "r") as f:
            principal_data = json.load(f)
            executor.submit(parse_json, principal_data, file, folder)
            # parse_json(principal_data, file, folder)


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


def main():
    first_t = timeit.default_timer()
    total_dirs = len(os.listdir(f"{MAIN_URL}"))
    for index, directorio in enumerate(sorted(os.listdir(f"{MAIN_URL}"), reverse=True)):
        path = f"{MAIN_URL}/{directorio}"
        print(f"directorio {path} num {index} de {total_dirs}")
        # for json_f in tqdm(os.listdir(f"{path}")):
        #     save_json_content(json_f, directorio)
        with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
            for json_f in tqdm(os.listdir(f"{path}")):
                executor.submit(save_json_content, json_f, directorio)

    last_t = timeit.default_timer()
    print("it took:", last_t - first_t)


def match_field(field: str, field_name: str):
    label_slug_filtered = StatementItemConcept.objects.filter(label_slug=field_name)
    if label_slug_filtered.exists():
        if label_slug_filtered.filter(corresponding_final_item="").exists():
            for item_field in label_slug_filtered:
                item_field.corresponding_final_item = field
                item_field.save(update_fields=["corresponding_final_item"])

def map_fields(field):
    field_name = field.replace("_field", "")
    field_filtered = StatementItemConcept.objects.filter(concept_slug=field_name)
    if field_filtered.exists():
        if field_filtered.filter(corresponding_final_item="").exists():
            for item_field in field_filtered:
                item_field.corresponding_final_item=field
                item_field.save(update_fields=["corresponding_final_item"])
    else:
        match_field(field, field_name)

def update_final():
    final = income_fields + balance_sheet_fields + cashflow_fields
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        for field in final:
            executor.submit(map_fields, field)

