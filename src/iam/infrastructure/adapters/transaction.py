from collections.abc import AsyncIterator, Sequence
from contextlib import asynccontextmanager
from typing import Any

from iam.application.ports.transaction import TransactionOf
from iam.infrastructure.in_memory_storage import (
    TransactionalInMemoryStorage,
)
from iam.infrastructure.sqlalchemy.driver import (
    PostgresDriver,
    single_session_of,
)


class InPostgresTransactionOf(TransactionOf[Sequence[PostgresDriver]]):
    @asynccontextmanager
    async def __call__(
        self, postgres_driver: Sequence[PostgresDriver]
    ) -> AsyncIterator[None]:
        async with single_session_of(postgres_driver).begin():
            yield


class InMemoryTransactionOf(
    TransactionOf[Sequence[TransactionalInMemoryStorage[Any]]]
):
    @asynccontextmanager
    async def __call__(
        self, storages: Sequence[TransactionalInMemoryStorage[Any]]
    ) -> AsyncIterator[None]:
        for storage in storages:
            storage.begin()

        try:
            yield
        except Exception as error:
            for storage in storages:
                storage.rollback()
            raise error from error
        else:
            for storage in storages:
                storage.commit()
