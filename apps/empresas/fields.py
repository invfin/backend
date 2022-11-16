from decimal import Decimal, InvalidOperation

from rest_framework.fields import DecimalField


class AccountingField(DecimalField):
    def __init__(
        self,
        *args,
        definition_path: str = "",
        spanish_version: str = "",
        spanish_snake_version: str = "",
        **kwargs,
    ):
        kwargs.setdefault("allow_null", True)
        self.definition_path = definition_path
        self.spanish_version = spanish_version
        self.spanish_snake_version = spanish_snake_version
        super().__init__(*args, **kwargs)

    def to_internal_value(self, data):
        if data is not None:
            try:
                data = Decimal(data)
            except InvalidOperation:
                self.fail("invalid")
            else:
                data = round(data, 2)

        return super().to_internal_value(data)
