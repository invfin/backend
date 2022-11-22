import json
from typing import Any

from django.db.models.expressions import Func


class JsonSetValue(Func):
    function = "jsonb_set"
    template = "%(function)s(%(field)s, '{\"%(key)s\"}','%(value)s', %(create_missing)s)"
    arity = 1

    def __init__(
        self,
        field: str,
        key: str,
        value: Any,
        create_missing: bool = True,
        **extra,
    ):
        super().__init__(
            field,
            key=key,
            value=value,
            create_missing="true" if create_missing else "false",
            **extra,
        )


class AddChecking(JsonSetValue):
    def __init__(self, key):
        super().__init__(
            field="checkings",
            key=f"has_{key}",
            value=json.dumps({"state": "no", "time": ""}),
        )
