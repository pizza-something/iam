from abc import ABC, abstractmethod
from dataclasses import dataclass

from iam.entities.access.account import Account


@dataclass(kw_only=True, frozen=True)
class Event: ...


@dataclass(kw_only=True, frozen=True)
class AccountCreatedEvent(Event):
    account: Account


class EventQueue(ABC):
    @abstractmethod
    async def push(self, event: Event) -> None: ...
