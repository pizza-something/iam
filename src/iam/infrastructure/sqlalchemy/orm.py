from typing import cast

from sqlalchemy.orm import (
    composite,
    registry,
)

from iam.entities.access.account import Account, AccountName
from iam.infrastructure.sqlalchemy.tables import account_table, metadata


def _mutable[T: type](type_: T) -> T:
    type_.__setattr__ = object.__setattr__  # type: ignore[method-assign, assignment]
    type_.__delattr__ = object.__delattr__  # type: ignore[method-assign, assignment]

    return type_


mapper_registry = registry(metadata=metadata)

mapper_registry.map_imperatively(
    _mutable(Account),
    account_table,
    properties=dict(
        id=account_table.c.id,
        name=composite(
            lambda text: AccountName(text=cast(str, text)),
            account_table.c.name_text,
        )
    ),
)
