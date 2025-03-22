from dataclasses import dataclass
from uuid import UUID, uuid4

from effect import Identified, New, new

from iam.entities.access.password import Password, PasswordHash, PasswordHashing


class EmptyAccountNameError(Exception): ...


@dataclass(kw_only=True, frozen=True)
class AccountName:
    """
    :raises iam.entities.access.account.EmptyAccountNameError:
    """

    text: str

    def __post_init__(self) -> None:
        if not self.text:
            raise EmptyAccountNameError


@dataclass(kw_only=True, frozen=True)
class Account(Identified[UUID]):
    id: UUID
    name: AccountName
    password_hash: PasswordHash


def registered_account_when(
    *,
    password_hashing: PasswordHashing,
    account_name: AccountName,
    password: Password,
) -> New[Account]:
    password_hash = password_hashing.hash_of(password)

    return new(Account(
        id=uuid4(), name=account_name, password_hash=password_hash
    ))
