from __future__ import annotations

from enum import Enum
from math import nan
from typing import Any, TypeVar

from django.core.files.uploadedfile import InMemoryUploadedFile
from pandas import DataFrame, read_csv, read_excel

from src.cartera.models import FirsttradeTransaction, Income, IngEsTransaction, Investment
from src.users.models import User

from .exceptions import FileProcessingError


T = TypeVar("T")

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

ING_COLUMNS_MAPPER = {
    "F. VALOR": "transaction_date",
    "CATEGORÍA": "category",
    "SUBCATEGORÍA": "subcaterogy",
    "DESCRIPCIÓN": "description",
    "COMENTARIO": "comment",
    "IMAGEN": "image",
    "IMPORTE (€)": "amount",
    "SALDO (€)": "balance",
}


class HandlerInterface:
    model: type[T]
    columns: dict[str, str]
    read_kwargs: dict[str, Any] = {}

    def get_models(self, transaction_file, user: User) -> list[T]:
        df = self._file_to_dataframe(transaction_file)
        df = df.rename(columns=self.columns).replace({nan: None})
        df = self._process_df(df)
        return self._prepare_models(df, transaction_file.name, user)

    def _file_to_dataframe(self, transaction_file) -> DataFrame:
        filename = transaction_file.name
        if filename.endswith(".csv"):
            reader = read_csv
        elif filename.endswith(".csv.gz"):
            self.read_kwargs["compression"] = "gzip"
            reader = read_csv
        elif filename.endswith(".xls"):
            reader = read_excel
        else:
            raise ValueError("File not recognized")
        return reader(transaction_file.file, **self.read_kwargs)

    def _process_df(self, df: DataFrame) -> DataFrame:
        return df

    def _prepare_models(self, df: DataFrame, filename: str, user: User):
        df["model"] = df.apply(
            func=self._create_transaction,
            axis=1,
            file_path=filename,
            model=self.model,
            user=user,
        )  # type: ignore
        return df.model.tolist()

    @staticmethod
    def _create_transaction(row: dict, model: type, file_path: str, user: User) -> Any:
        return model(**row, file_path=file_path, user=user)


class Firsttrade(HandlerInterface):
    model: type[FirsttradeTransaction] = FirsttradeTransaction
    columns: dict[str, str] = FIRSTTRADE_COLUMNS_MAPPER

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


class Ing(HandlerInterface):
    model: type[IngEsTransaction] = IngEsTransaction
    columns: dict[str, str] = ING_COLUMNS_MAPPER
    read_kwargs = {"skiprows": list(range(5))}

    def _process_df(self, df: DataFrame) -> DataFrame:
        df["image"] = df["image"].replace({"No": None})
        df["currency_id"] = 3
        return df


class FileTransactionsHandler(str, Enum):
    PERSONAL = "Personal"
    FIRSTRADE = "Firsttrade"
    ING = "ING"

    @classmethod
    def create(
        cls,
        origin: str,
        transactions_file: InMemoryUploadedFile,
        user: User,
    ):
        try:
            user = User.objects.get(id=1)
            handler = cls(origin)
            return handler._create_models(handler._get_handler(), transactions_file, user)
        except Exception as e:
            raise FileProcessingError(f"Error processing file: {str(e)}") from e

    def _create_models(
        self,
        handler,
        transactions_file: InMemoryUploadedFile,
        user: User,
    ):
        models = handler().get_models(transactions_file, user)
        return handler.model.objects.bulk_create(models)

    def _get_handler(self):
        return {self.FIRSTRADE: Firsttrade, self.ING: Ing}[self]


class FileTransactionsType(Enum):
    INCOME = "income"
    SPEND = "spend"
    INVESTMENT = "investment"
    SAVING = "saving"
