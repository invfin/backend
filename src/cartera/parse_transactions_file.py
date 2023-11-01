from pandas import read_csv

from src.cartera.models import FirsttradeTransaction

column_mapping = {
    "Symbol": "symbol",
    "Quantity": "quantity",
    "Price": "price",
    "Action": "action",
    "Description": "description",
    "TradeDate": "trade_date",
    "SettledDate": "settled_date",
    "Interest": "interest",
    "Amount": "amount",
    "Commission": "commission",
    "Fee": "fee",
    "CUSIP": "cusip",
    "RecordType": "record_type",
}


def _create_transaction(row: dict, filename: str):
    return FirsttradeTransaction(**row, filename=filename)


def parse_file(filename: str):
    if filename.endswith(".csv"):
        df = read_csv(filename).rename(columns=column_mapping)
        df["model"] = df.apply(f=_create_transaction, axis=1, filename=filename)
        FirsttradeTransaction.objects.bulk_create(df.model)
    else:
        raise ValueError("Wrong file format")


def _save_file():
    pass
