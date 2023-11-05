from __future__ import annotations

from enum import Enum
from math import nan
from typing import Any, Dict

from django.core.files.uploadedfile import InMemoryUploadedFile
from pandas import DataFrame, read_csv

from src.cartera.models import FirsttradeTransaction, Income, Investment
from src.users.models import User

from .exceptions import FileProcessingError

FIRSTTRADE_COLUMNS_MAPPER = {
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


class Firsttrade:
    model: type[FirsttradeTransaction] = FirsttradeTransaction
    columns: Dict[str, str] = FIRSTTRADE_COLUMNS_MAPPER

    class Action(str, Enum):
        BUY = "BUY"
        SELL = "SELL"
        INTEREST = "INTEREST"
        DIVIDEND = "DIVIDEND"

        def __new__(cls, value: str) -> Firsttrade.Action:
            return super().__new__(cls, value.upper())

    def _model(self, action: Firsttrade.Action):
        if action in {Firsttrade.Action.DIVIDEND, Firsttrade.Action.INTEREST}:
            return Income
        return Investment


class ING:
    pass


class FileTransactionsSource(str, Enum):
    PERSONAL = "Personal"
    FIRSTRADE = "Firsttrade"
    ING = "ING"

    def handler(self):
        return {self.FIRSTRADE: Firsttrade}[self]


class FileTransactionsType(Enum):
    INCOME = "income"
    SPEND = "spend"
    INVESTMENT = "investment"
    SAVING = "saving"


class FileTransactionsHandler:
    handler: type[Firsttrade]
    transactions_file: InMemoryUploadedFile
    filename: str
    user: User

    def __init__(
        self,
        origin: str,
        transactions_file: InMemoryUploadedFile,
        user: User,
    ):
        self.handler = FileTransactionsSource(origin).handler()
        self.transactions_file = transactions_file
        self.filename = transactions_file.name
        # self.user = user TODO: use this once the user is taken from the jwt
        self.user = User.objects.get(id=1)

    def create(self):
        try:
            return self._create_models()
        except Exception as e:
            raise FileProcessingError(f"Error processing file: {str(e)}") from e

    def _create_models(self):
        model = self.handler.model
        columns = self.handler.columns
        return model.objects.bulk_create(self._prepare_models(model, columns, self.user))

    def _prepare_models(self, model: type, columns: Dict[str, str], user: User):
        df = self._file_to_dataframe().rename(columns=columns).replace({nan: None})
        df["model"] = df.apply(
            func=self._create_transaction,
            axis=1,
            file_path=self.filename,
            model=model,
            user=user,
        )  # type: ignore
        return df.model.tolist()

    def _file_to_dataframe(self) -> DataFrame:
        if self.filename.endswith(".csv"):
            return read_csv(self.transactions_file.file)
        elif self.filename.endswith(".csv.gz"):
            return read_csv(self.transactions_file.file, compression="gzip")
        else:
            raise ValueError("File not recognized")

    @staticmethod
    def _create_transaction(row: dict, model: type, file_path: str, user: User) -> Any:
        return model(**row, file_path=file_path, user=user)
