from __future__ import annotations

import logging
from decimal import Decimal
from enum import Enum
from functools import partial
from math import isnan, nan

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models import Model
from pandas import DataFrame, Series, read_csv, read_excel

from src.cartera.constants import InvestmentMovement
from src.cartera.models import (
    CashflowMovementCategory,
    FirsttradeTransaction,
    Income,
    IngEsTransaction,
    Investment,
    NetWorth,
    Savings,
    Spendings,
    WireTransfer,
)
from src.empresas.models.company import Company
from src.users.models import User
from .facades import NetWorthFacade

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
logger = logging.getLogger(__name__)
TransactionType = Spendings | Investment | Income | Savings
RawTransactionType = FirsttradeTransaction | IngEsTransaction


class RawModelToStdModel:
    def create_relationship(self, instances: list[RawTransactionType]) -> None:
        net_worths: set[NetWorth] = set()
        for instance in instances:
            if new_transaction := self._raw_to_std(instance):
                net_worth = NetWorthFacade(instance.user, new_transaction.date).net_worth
                new_transaction.net_worth = net_worth
                new_transaction.save()
                net_worths.add(net_worth)
        NetWorthFacade.update_many(net_worths)

    def _save_to_movements(
        self,
        class_: Model,
        movement: Model,
        movements: dict[str, list[Model]],
    ) -> None:
        movements[class_.__class__.__name__].append(movement)

    def _raw_to_std(self, model: RawTransactionType) -> TransactionType:
        ...

    def _to_spendings(self, *args, **kwargs) -> Spendings:
        ...

    def _to_income(self, *args, **kwargs) -> Income:
        ...

    def _to_investment(self, *args, **kwargs) -> Investment:
        ...

    def _to_savings(self, *args, **kwargs) -> Savings:
        ...

    def _to_wire_transfer(self, *args, **kwargs) -> WireTransfer:
        ...


class FileToRawModelInterface:
    model: RawTransactionType
    columns: dict[str, str]
    fields_to_exclude: set[str] = {"id", "category_id", "created_at", "updated_at"}
    read_kwargs: dict = {}

    def create_raw_models(
        self,
        transactions_file: InMemoryUploadedFile,
        user: User,
    ) -> list[RawTransactionType]:
        return self._get_models(transactions_file, user)

    def _get_models(
        self,
        transaction_file: InMemoryUploadedFile,
        user: User,
    ) -> list[RawTransactionType]:
        df = self._file_to_dataframe(transaction_file)
        df = df.rename(columns=self.columns).replace({nan: None})
        df = self._process_df(df)
        return self._prepare_models(df, transaction_file.name, user)

    def _file_to_dataframe(self, transaction_file: InMemoryUploadedFile) -> DataFrame:
        filename = transaction_file.name
        if filename.endswith(".csv"):
            reader = partial(read_csv)
        elif filename.endswith(".csv.gz"):
            reader = partial(read_csv, compression="gzip")
        elif filename.endswith(".xls"):
            reader = partial(read_excel, **self.read_kwargs)
        else:
            raise ValueError("File not recognized")
        return reader(transaction_file.file)

    def _process_df(self, df: DataFrame) -> DataFrame:
        return df

    @staticmethod
    def to_decimal(v):
        if v and not isnan(v):
            return Decimal(v)
        return Decimal("0.0")

    def _prepare_models(self, df: DataFrame, filename: str, user: User):
        df["model"] = df.apply(
            func=self._create_transaction,
            axis=1,
            file_path=filename,
            model=self.model,
            user=user,
        )  # type: ignore
        return df.model.tolist()

    @classmethod
    def _create_transaction(
        cls,
        row: Series,
        model: RawTransactionType,
        file_path: str,
        user: User,
    ) -> RawTransactionType:
        data = cls._filter_data(row)
        try:
            instance, _ = model.objects.get_or_create(
                file_path=file_path,
                user=user,
                **data,
            )
            return instance
        except model.MultipleObjectsReturned:
            instance = model.objects.filter(**data, file_path=file_path, user=user).first()
            if not instance:
                raise ValueError("_create_transaction no model")
            return instance

    @classmethod
    def _filter_data(cls, data: Series) -> dict:
        d = data.to_dict()
        for k in d.keys():
            if isinstance(d[k], Decimal):
                d[k] = Decimal(d[k]).quantize(Decimal("1.000"))
        return d


class Firsttrade(FileToRawModelInterface, RawModelToStdModel):
    model = FirsttradeTransaction
    columns: dict[str, str] = FIRSTTRADE_COLUMNS_MAPPER

    class Action(str, Enum):
        BUY = "BUY"
        SELL = "SELL"
        INTEREST = "INTEREST"
        DIVIDEND = "DIVIDEND"
        OTHER = "OTHER"

        def _is_income(self) -> bool:
            return self in {self.DIVIDEND, self.INTEREST}

        def _is_investment(self) -> bool:
            return self in {self.BUY, self.SELL}

    def _process_df(self, df: DataFrame) -> DataFrame:
        df["symbol"] = df["symbol"].str.strip()
        df["description"] = df["description"].str.strip()
        df["cusip"] = df["cusip"].str.strip()
        for col in ("price", "interest", "quantity", "commission", "fee", "amount"):
            df[col] = df[col].apply(self.to_decimal)
        return df

    def _raw_to_std(self, model: FirsttradeTransaction):
        action = Firsttrade.Action(model.action.upper())
        if action._is_income():
            func = self._to_income
            # TODO: check if when sending funds to bank account is the same starting
        elif action._is_investment() or model.description.startswith("Wire Funds"):
            func = self._to_investment
        elif model.description.startswith(("***", "INTEREST ON CREDIT")):
            func = self._to_spendings
        else:
            return
        return func(model, action)

    def _to_spendings(self, model: FirsttradeTransaction, *args) -> Spendings:
        return Spendings(
            user=model.user,
            name=model.description.replace("***", ""),
            amount=abs(model.amount),
            description=model.description,
            date=model.settled_date,
            currency_id=1,
            transaction_file=model,
        )

    def _to_income(self, model: FirsttradeTransaction, action: Firsttrade.Action) -> Income:
        name, company_info = model.description, {}

        if action == Firsttrade.Action.INTEREST:
            interest_title = "INTEREST ON CREDIT BALANCE"
            cat, _ = CashflowMovementCategory.objects.get_or_create(name="Interests")
            if model.description.startswith(interest_title):
                name = interest_title.title()
            else:
                name = "".join(model.description.split()[:3])
        elif action == Firsttrade.Action.DIVIDEND:
            name = f"Dividendo: {model.symbol}"
            cat, _ = CashflowMovementCategory.objects.get_or_create(name="Dividends")
            company_info["object"] = self._get_company(model.symbol)

        return Income(
            user=model.user,
            name=name,
            amount=model.amount,
            description=model.description,
            date=model.settled_date,
            currency_id=1,
            category=cat,
            transaction_file=model,
            to_substract=True,
            **company_info,
        )

    def _get_company(self, ticker: str) -> Company:
        company, _ = Company.objects.find_or_create(ticker, Company.objects.get)  # type: ignore
        return company

    def _to_investment(
        self,
        model: FirsttradeTransaction,
        action: Firsttrade.Action,
    ) -> Investment:
        if action == Firsttrade.Action.OTHER:
            cat, _ = CashflowMovementCategory.objects.get_or_create(name="Wire Transfers")
            if model.description.startswith("Wire Funds Received"):
                name = "Fondos recibidos"
                movement = InvestmentMovement.RECEIVE_FUND
            else:
                name = "Fondos enviados"
                movement = InvestmentMovement.SEND_FUND
        else:
            cat = None
            name = "Compra: {}" if action == Firsttrade.Action.BUY else "Venta {}"
            name = name.format(model.symbol)
            movement = InvestmentMovement(action.value)

        return Investment(
            user=model.user,
            name=name,
            object=self._get_asset(model.symbol),
            quantity=model.quantity,
            price=model.price,
            movement=movement,
            category=cat,
            amount=abs(model.amount),
            description=model.description,
            date=model.settled_date,
            currency_id=1,
            transaction_file=model,
        )

    def _get_asset(self, ticker: str) -> Company:
        company, _ = Company.objects.find_or_create(  # type: ignore
            ticker.strip().upper(),
            Company.objects.get,
        )
        return company


class Ing(FileToRawModelInterface, RawModelToStdModel):
    model: type[IngEsTransaction] = IngEsTransaction
    columns: dict[str, str] = ING_COLUMNS_MAPPER
    read_kwargs = {"skiprows": 5}

    def _process_df(self, df: DataFrame) -> DataFrame:
        df["image"] = df["image"].replace({"No": ""})
        df["comment"] = df["comment"].replace({nan: ""})
        df["currency_id"] = 5
        for col in ("amount", "balance"):
            df[col] = df[col].apply(self.to_decimal)
        return df

    def _raw_to_std(self, model: IngEsTransaction):
        func = self._to_income if model.amount > 0 else self._to_spendings
        return func(model)

    def _to_spendings(self, model: IngEsTransaction) -> Spendings:
        return Spendings(
            user=model.user,
            name=model.description,
            amount=abs(model.amount),
            description=model.description,
            date=model.transaction_date,
            currency=model.currency,
            transaction_file=model,
        )

    def _to_income(self, model: IngEsTransaction) -> Income:
        return Income(
            user=model.user,
            name=model.description,
            amount=abs(model.amount),
            description=model.description,
            date=model.transaction_date,
            currency=model.currency,
            transaction_file=model,
        )


class FileTransactionsHandler(str, Enum):
    PERSONAL = "Personal"
    FIRSTRADE = "Firsttrade"
    ING = "ING"

    def create(
        self,
        transactions_file: InMemoryUploadedFile,
        user: User,
    ) -> list[RawTransactionType]:
        user = User.objects.get(id=1)
        return self._create_models(transactions_file, user)

    # try:
    #     user = User.objects.get(id=1)
    #     return self._create_models(transactions_file, user)
    # except Exception as e:
    #     raise FileProcessingError(f"Error processing file: {str(e)}") from e

    def _create_models(
        self,
        transactions_file: InMemoryUploadedFile,
        user: User,
    ) -> list[RawTransactionType]:
        handler = self._get_handler()
        models = handler.create_raw_models(transactions_file, user)
        handler.create_relationship(models)
        return models

    def _get_handler(self) -> Firsttrade | Ing:
        handlers = {self.FIRSTRADE: Firsttrade, self.ING: Ing}
        handler = handlers[self]
        return handler()
