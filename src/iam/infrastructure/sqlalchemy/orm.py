from typing import cast

from sqlalchemy.orm import (
    composite,
    registry,
)

from iam.entities.access.account import Account, AccountName
from iam.entities.access.password import PasswordHash
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
        ),
        password_hash=composite(
            lambda text: PasswordHash(text=cast(str, text)),
            account_table.c.password_hash_text,
        ),
    ),
)

_mutable(AccountName).__composite_values__ = lambda self: (self.text,)  # type: ignore[attr-defined]
_mutable(PasswordHash).__composite_values__ = lambda self: (self.text,)  # type: ignore[attr-defined]
