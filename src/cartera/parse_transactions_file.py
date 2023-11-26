from __future__ import annotations

import datetime
import logging
from decimal import Decimal
from enum import Enum
from functools import cached_property
from math import nan
from typing import Any, Generator

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models import Manager, Model
from pandas import DataFrame, read_csv, read_excel

from src.cartera.constants import InvestmentMovement
from src.cartera.models import (
    FirsttradeTransaction,
    Income,
    IngEsTransaction,
    Investment,
    NetWorth,
    Savings,
    Spendings,
)
from src.currencies.facades import ExchangeRateFacade
from src.currencies.models import Currency, UserDefaultCurrency
from src.empresas.models.company import Company
from src.periods.models import Period
from src.periods.outils import FiscalDate
from src.users.models import User

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


class AmountToConvert:
    def __init__(self, pk: int, amount: Decimal, currency__code: str, date: datetime.date):
        self.pk = pk
        self.amount = amount
        self.base = currency__code
        self.date = date


class BatchTransactionsToConvert:
    def __init__(self, manager: Manager) -> None:
        self.manager = manager

    @classmethod
    def get_batch(cls, net_worth: NetWorth):
        managers = [
            net_worth.net_worth_incomes,  # type: ignore
            net_worth.net_worth_savings,  # type: ignore
            net_worth.net_worth_spendings,  # type: ignore
            net_worth.net_worth_investments,  # type: ignore
        ]
        for manager in managers:
            yield cls(manager)

    def amounts(self) -> Generator[AmountToConvert, None, None]:
        values = "pk", "amount", "currency__code", "date"
        for i in (
            self.manager.prefetch_related("currency").values(*values).iterator(chunk_size=100)
        ):
            yield AmountToConvert(**i)


class NetWorthFacade:
    def __init__(
        self,
        user: User | None = None,
        date: datetime.date | None = None,
        net_worth: NetWorth | None = None,
    ):
        if net_worth:
            self.net_worth = net_worth
        elif user and date:
            period = FiscalDate(date).period
            self.net_worth, _ = self.get(user, period)
        else:
            logging.error(f"user: {vars(user)}, date: {date}, net_worth: {vars(net_worth)}")
            raise ValueError("Invalid networth")
        return None

    @classmethod
    def update_many(cls, net_worths: set[NetWorth]):
        for net_worth in net_worths:
            cls(net_worth=net_worth).update()
        return None

    def update(self):
        target_currency = self._get_target_currency()
        self._convert_amounts(target_currency)

    def _get_target_currency(self) -> Currency:
        try:
            return self.net_worth.user.currency.currency  # type: ignore
        except Exception as e:
            currency = UserDefaultCurrency.objects.create(
                user=self.net_worth.user, currency_id=5
            )
            logger.error(str(e))
            return currency.currency

    def _convert_amounts(self, target: Currency) -> None:
        for batch in BatchTransactionsToConvert.get_batch(self.net_worth):
            for amount_to_convert in batch.amounts():
                try:
                    amount_converted = ExchangeRateFacade(
                        pk=amount_to_convert.pk,
                        base=amount_to_convert.base,
                        target=target.code,
                        target_pk=target.pk,
                        date=amount_to_convert.date,
                    ).convert(amount_to_convert.amount)
                    batch.manager.filter(id=amount_to_convert.pk).update(
                        read=True,
                        amount_converted=amount_converted,
                    )
                except ValueError as e:
                    logger.error(f"{vars(amount_to_convert)} error: {str(e)}")

    def get(self, user: User, period: Period) -> tuple[NetWorth, bool]:
        return NetWorth.objects.get_or_create(user=user, period=period)


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

    def _raw_to_std(self, model: RawTransactionType) -> TransactionType: ...

    def __to_spendings(self, *args, **kwargs) -> Spendings: ...

    def _to_income(self, *args, **kwargs) -> Income: ...

    def _to_investment(self, *args, **kwargs) -> Investment: ...

    def __to_savings(self, *args, **kwargs) -> Savings: ...


class FileToRawModelInterface:
    model: RawTransactionType
    columns: dict[str, str]
    read_kwargs: dict[str, Any] = {}
    fields_to_exclude: set[str] = {"id", "category_id", "created_at", "updated_at"}

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
            reader = read_csv
        elif filename.endswith(".csv.gz"):
            k = self.read_kwargs.copy()
            k["compression"] = "gzip"
            self.read_kwargs = k
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
    def _create_transaction(
        row: dict,
        model: RawTransactionType,
        file_path: str,
        user: User,
    ) -> RawTransactionType:
        try:
            instance, _ = model.objects.get_or_create(
                **row,
                file_path=file_path,
                user=user,
            )
            return instance
        except model.MultipleObjectsReturned:
            instance = model.objects.filter(**row, file_path=file_path, user=user).first()
            if not instance:
                raise ValueError("_create_transaction no model")
            return instance


class Firsttrade(FileToRawModelInterface, RawModelToStdModel):
    model: type[FirsttradeTransaction] = FirsttradeTransaction
    columns: dict[str, str] = FIRSTTRADE_COLUMNS_MAPPER

    class Action(str, Enum):
        BUY = "BUY"
        SELL = "SELL"
        INTEREST = "INTEREST"
        DIVIDEND = "DIVIDEND"
        OTHER = "OTHER"

        @cached_property
        def _is_income(self) -> bool:
            return self in {self.DIVIDEND, self.INTEREST}

        @cached_property
        def _is_investment(self) -> bool:
            return self in {self.BUY, self.SELL}

    def _process_df(self, df: DataFrame) -> DataFrame:
        df["symbol"] = df["symbol"].str.strip()
        return df

    def _raw_to_std(self, model: FirsttradeTransaction):
        action = Firsttrade.Action(model.action.upper())
        if action._is_income:
            func = self._to_income
        elif action._is_investment:
            func = self._to_investment
        elif model.description.startswith(("***", "INTEREST ON CREDIT")):
            func = self.__to_spendings
        else:
            return
        return func(model, action)

    def __to_spendings(self, model: FirsttradeTransaction, *args) -> Spendings:
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
        name = model.description
        company, company_info = None, {}
        if action == Firsttrade.Action.INTEREST:
            interest_title = "INTEREST ON CREDIT BALANCE"
            if model.description.startswith(interest_title):
                name = interest_title.title()
            else:
                name = "".join(model.description.split()[:3])
        elif action == Firsttrade.Action.DIVIDEND:
            name = f"Dividendo: {model.symbol}"
            company = self._get_company(model.symbol)
            company_info["object"] = company

        return Income(
            user=model.user,
            name=name,
            amount=model.amount,
            description=model.description,
            date=model.settled_date,
            currency_id=1,
            transaction_file=model,
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
        name = "Compra: {}" if action == Firsttrade.Action.BUY else "Venta {}"
        return Investment(
            user=model.user,
            name=name.format(model.symbol),
            object=self._get_asset(model.symbol),
            quantity=model.quantity,
            price=model.price,
            movement=InvestmentMovement(action.value),
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
    read_kwargs = {"skiprows": list(range(5))}

    def _process_df(self, df: DataFrame) -> DataFrame:
        df["image"] = df["image"].replace({"No": ""})
        df["comment"] = df["comment"].replace({nan: ""})
        df["currency_id"] = 5
        return df

    def _raw_to_std(self, model: IngEsTransaction):
        if model.amount > 0:
            func = self._to_income
        else:
            func = self.__to_spendings

        return func(model)

    def __to_spendings(self, model: IngEsTransaction) -> Spendings:
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
