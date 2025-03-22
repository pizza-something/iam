from abc import ABC, abstractmethod
from collections.abc import Sequence
from contextlib import AbstractAsyncContextManager
from typing import Any


type Transaction = AbstractAsyncContextManager[Any]


class TransactionOf[StoragesT: Sequence[Any]](ABC):
    @abstractmethod
    def __call__(self, storages: StoragesT) -> Transaction: ...
