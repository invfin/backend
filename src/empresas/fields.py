from typing import Any

from django.db.models import FloatField


class EntryStatementField(FloatField):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        kwargs["blank"] = True
        kwargs["default"] = 0
        kwargs["null"] = True
        super().__init__(*args, **kwargs)
