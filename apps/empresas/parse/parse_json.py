import os, json, re, concurrent.futures, datetime


from apps.empresas.models import (
    Company,
    IncomeStatementAsReported,
    BalanceSheetAsReported,
    CashflowStatementAsReported,
)
from apps.general.models import Period, Currency
from apps.general import constants

main_url = "/home/lucas/Downloads/kaggle-companies-data"


pattern = re.compile(r"(?<!^)(?=[A-Z])")


def camel_to_snake(word):
    return pattern.sub("_", word).lower().replace(":", "")


def save_into_dict(dict_to_save, dict_to_use):
    concept = dict_to_save["concept"]
    label = dict_to_save["label"]
    if concept in dict_to_use:
        if label in dict_to_use[concept]["labels"]:
            dict_to_use[concept]["labels"][label] += 1
        else:
            dict_to_use[concept]["labels"].update({label: 0})
    else:
        dict_to_use[concept] = {"concept": camel_to_snake(concept), "labels": {label: 0}}


def save_lists(data, company, period, start_date, end_date):
    cashflow = data["cf"]
    balance = data["bs"]
    income = data["ic"]
    info_inc_dict = dict()
    info_bs_dict = dict()
    info_cf_dict = dict()
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
                        currency = Currency.objects.get_or_create(currency=currency_str.upper())
                    except Currency.MultipleObjectsReturned:
                        currency = Currency.objects.filter(currency=currency_str.upper()).first()
        info_inc_dict.update(info_inc)
        info_bs_dict.update(info_bs)
        info_cf_dict.update(info_cf)
    IncomeStatementAsReported.objects.create(
        company=company,
        period=period,
        financial_data=info_inc_dict,
        reported_currency=currency,
        start_date=start_date,
        end_date=end_date,
    )
    BalanceSheetAsReported.objects.create(
        company=company,
        period=period,
        financial_data=info_bs_dict,
        reported_currency=currency,
        start_date=start_date,
        end_date=end_date,
    )
    CashflowStatementAsReported.objects.create(
        company=company,
        period=period,
        financial_data=info_cf_dict,
        reported_currency=currency,
        start_date=start_date,
        end_date=end_date,
    )


def get_period(quarter):
    if quarter == "Q1":
        period = constants.PERIOD_1_QUARTER
    elif quarter == "Q2":
        period = constants.PERIOD_2_QUARTER
    elif quarter == "Q3":
        period = constants.PERIOD_3_QUARTER
    elif quarter == "FY":
        period = constants.PERIOD_FOR_YEAR
    return period


def save_json_content(file):
    # we open the json and access to the data
    json_info_file = f"{main_url}/{dir}/{file}"
    with open(json_info_file, "r") as f:
        principal_data = json.load(f)
        year = principal_data["year"]
        start_date = datetime.datetime.strptime(principal_data["startDate"], "%Y-%m-%d").date()
        end_date = datetime.datetime.strptime(principal_data["endDate"], "%Y-%m-%d").date()
        data = principal_data["data"]
        company, created = Company.objects.get_or_create(
            ticker=principal_data["symbol"], defaults={"name": "From-as-reported"}
        )
        period = get_period(principal_data["quarter"])
        period_obj = Period.objects.get(year=int(year), period=period)
        save_lists(data, company, period_obj, start_date, end_date)


def main():
    # loop over folders
    for dir in sorted(os.listdir(f"{main_url}")):
        jsons_all = sorted(os.listdir(f"{main_url}/{dir}"))
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(save_json_content, jsons_all)


if __name__ == "__main__":
    main()
