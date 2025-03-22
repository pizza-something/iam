from abc import ABC, abstractmethod
from dataclasses import dataclass, field


class WeekPasswordError(Exception): ...


class ShortPasswordError(WeekPasswordError): ...


@dataclass(kw_only=True, frozen=True)
class Password:
    """
    :raises iam.entities.access.password.ShortPasswordError:
    """

    text: str = field(repr=False)

    def __post_init__(self) -> None:
        if len(self.text) < 8:
            raise ShortPasswordError


@dataclass(kw_only=True, frozen=True)
class PasswordHash:
    text: str


class PasswordHashing(ABC):
    @abstractmethod
    def hash_of(self, password: Password) -> PasswordHash: ...

    @abstractmethod
    def is_hash_valid(
        self,
        password_hash: PasswordHash,
        *,
        password: Password,
    ) -> bool: ...
