from abc import ABC, abstractmethod
from typing import Self
from uuid import UUID

from pydantic import BaseModel

from iam.entities.access.account import Account


class OutputSchema[ValueT](BaseModel, ABC):
    @classmethod
    @abstractmethod
    def of(cls, value: ValueT, /) -> Self: ...


class OutputAccountSchema(OutputSchema[Account]):
    id: UUID

    @classmethod
    def of(cls, account: Account) -> "OutputAccountSchema":
        return OutputAccountSchema(id=account.id)
