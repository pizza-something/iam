from abc import ABC, abstractmethod

from iam.entities.access.account import Account, AccountName


class Accounts(ABC):
    @abstractmethod
    async def account_with_name(self, name: AccountName) -> Account | None: ...
