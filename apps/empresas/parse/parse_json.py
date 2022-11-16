import os, json, re, concurrent.futures, datetime, timeit, random

from tqdm import tqdm

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


def camel_to_snake(word):
    return pattern.sub("_", word).lower().replace(":", "")


def save_item_concept(concept, label, company) -> StatementItemConcept:
    slug = camel_to_snake(concept)
    try:
        item_concept = StatementItemConcept.objects.get(
            concept=concept,
            label=label,
            slug=slug,
        )
    except StatementItemConcept.DoesNotExist:
        if concept.startswith(company.ticker.lower()):
            item_concept = StatementItemConcept.objects.create(
                concept=concept,
                label=label,
                slug=slug,
                company=company,
            )
        else:
            item_concept = StatementItemConcept.objects.create(
                concept=concept,
                label=label,
                slug=slug,
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


def save_json_content(file, folder):
    # we open the json and access to the data
    json_info_file = f"{MAIN_URL}/{folder}/{file}"
    with open(f"{json_info_file}", "r") as f:
        principal_data = json.load(f)
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


def main():
    first_t = timeit.default_timer()
    for directorio in tqdm(os.listdir(f"{MAIN_URL}")):
        path = f"{MAIN_URL}/{directorio}"
        with concurrent.futures.ProcessPoolExecutor() as executor:
            for json_f in tqdm(os.listdir(f"{path}")):
                executor.submit(save_json_content, json_f, directorio)
                # save_json_content(f"{path}/{json_f}")
    last_t = timeit.default_timer()
    print("it took:", last_t - first_t)
