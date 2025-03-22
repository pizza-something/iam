from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import Any

from effect import LifeCycle

from iam.entities.access.account import Account


type StoredEntityLifeCycle = LifeCycle[Account]


class NotUniqueAccountNameError(Exception): ...


class MapTo[StoragesT: Sequence[Any]](ABC):
    @abstractmethod
    async def __call__(
        self,
        storages: StoragesT,
        effect: StoredEntityLifeCycle,
    ) -> None:
        """
        :raises iam.application.ports.map.NotUniqueAccountNameError:
        """
