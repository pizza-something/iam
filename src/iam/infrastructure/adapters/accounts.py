from dataclasses import dataclass
from typing import cast
from uuid import UUID

from sqlalchemy import select

from iam.application.ports.accounts import Accounts
from iam.entities.access.account import Account, AccountName
from iam.infrastructure.in_memory_storage import TransactionalInMemoryStorage
from iam.infrastructure.sqlalchemy.driver import PostgresDriver
from iam.infrastructure.sqlalchemy.tables import account_table


@dataclass(kw_only=True, slots=True)
class InMemoryAccounts(TransactionalInMemoryStorage[Account]):
    async def account_with_id(self, id: UUID) -> Account | None:
        for account in self._storage:
            if account.id == id:
                return account

        return None


@dataclass(kw_only=True, frozen=True, slots=True)
class InPostgresAccounts(Accounts, PostgresDriver):
    async def account_with_name(self, name: AccountName) -> Account | None:
        stmt = select(Account).where(account_table.c.name_text == name.text)

        return cast(Account | None, await self.session.scalar(stmt))
