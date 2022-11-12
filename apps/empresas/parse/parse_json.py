import os, json, re, concurrent.futures, datetime, timeit, random

from tqdm import tqdm

from apps.empresas.models import (
    Company,
    IncomeStatementAsReported,
    BalanceSheetAsReported,
    CashflowStatementAsReported,
)
from apps.periods.models import Period
from apps.currencies.models import Currency
from apps.periods import constants

pattern = re.compile(r"(?<!^)(?=[A-Z])")

MAIN_URL = "/home/lucas/Downloads/kaggle-companies-data"


def camel_to_snake(word):
    return pattern.sub("_", word).lower().replace(":", "")


def save_into_dict(dict_to_save, dict_to_use):
    original_concept = dict_to_save["concept"]
    concept = original_concept
    if concept in dict_to_use:
        concept = f"{concept}_duplicated"
        if concept in dict_to_use:
            num = random.randint(0, 9999999)
            concept = f"{concept}_{num}"
    dict_to_use[concept] = {**dict_to_save, "snake_concept": camel_to_snake(original_concept)}


def save_fields(file_name, data):
    original_concept = data["concept"]
    with open(f"./{file_name}.json", "r") as read_checks_json:
        checks_json = json.load(read_checks_json)
    checks_json.update({original_concept: "x"})
    with open(f"./{file_name}.json", "w") as writte_checks_json:
        json.dump(checks_json, writte_checks_json, indent=2, separators=(",", ": "))


def save_lists(data, company, period, start_date, end_date, file, folder):
    cashflow = data["cf"]
    balance = data["bs"]
    income = data["ic"]
    info_inc_dict = {}
    info_bs_dict = {}
    info_cf_dict = {}
    currency = None
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

        save_into_dict(info_inc, info_inc_dict)
        save_into_dict(info_bs, info_bs_dict)
        save_into_dict(info_cf, info_cf_dict)
        # save_fields("info_inc", info_inc)
        # save_fields("info_bs", info_bs)
        # save_fields("info_cf", info_cf)

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

    IncomeStatementAsReported.objects.create(financial_data=info_inc_dict, **data_shared_dict)
    BalanceSheetAsReported.objects.create(financial_data=info_bs_dict, **data_shared_dict)
    CashflowStatementAsReported.objects.create(financial_data=info_cf_dict, **data_shared_dict)


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
