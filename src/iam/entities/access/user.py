from dataclasses import dataclass

from effect import Effect, just

from iam.entities.access.account import (
    Account,
    AccountName,
    registered_account_when,
)
from iam.entities.access.password import Password, PasswordHashing
from iam.entities.access.session import (
    Session,
    extended,
    is_active,
    new_session_when,
)
from iam.entities.time.time import Time


@dataclass(kw_only=True, frozen=True)
class SignedUpUser:
    session: Session


def signed_up_user_when(
    *,
    current_time: Time,
    password_hashing: PasswordHashing,
    account_name: AccountName,
    password: Password,
) -> Effect[SignedUpUser, Account]:
    account = registered_account_when(
        password_hashing=password_hashing,
        account_name=account_name,
        password=password,
    )

    return account.map(lambda _: SignedUpUser(
        session=new_session_when(
            account_id=just(account).id, current_time=current_time
        )
    ))


type PrimaryAuthenticatedUser = None
primary_authenticated_user: PrimaryAuthenticatedUser = None


class InvalidPasswordForPrimaryAuthenticatedUserError(Exception): ...


def primary_authenticated_user_when(
    *,
    account: Account,
    password: Password,
    password_hashing: PasswordHashing,
) -> PrimaryAuthenticatedUser:
    """
    :raises iam.entities.access.user.InvalidPasswordForPrimaryAuthenticatedUserError:
    """  # noqa: E501

    is_password_valid = (
        password_hashing.is_hash_valid(account.password_hash, password=password)
    )

    if not is_password_valid:
        raise InvalidPasswordForPrimaryAuthenticatedUserError

    return primary_authenticated_user


@dataclass(kw_only=True, frozen=True)
class SignedInUser:
    session: Session


class InvalidPasswordForSignedInUserError(Exception): ...


def signed_in_user_when(
    *,
    current_time: Time,
    password_hashing: PasswordHashing,
    account: Account,
    password: Password,
) -> SignedInUser:
    """
    :raises iam.entities.access.user.InvalidPasswordForPrimaryAuthenticatedUserError:
    """  # noqa: E501

    primary_authenticated_user_when(
        account=account, password=password, password_hashing=password_hashing
    )
    session = new_session_when(account_id=account.id, current_time=current_time)

    return SignedInUser(session=session)


@dataclass(kw_only=True, frozen=True)
class UserWithExtendedSession:
    session: Session


class NotActiveSessionForUserWithExtendedSessionError(Exception): ...


def user_with_extended_session_when(
    *,
    current_time: Time,
    session: Session,
) -> UserWithExtendedSession:
    """
    :raises iam.entities.access.user.NotActiveSessionForUserWithExtendedSessionError:
    :raises iam.entities.access.session.NotExtendableSessionForExtendedSessionError:
    """  # noqa: E501

    if not is_active(session, current_time=current_time):
        raise NotActiveSessionForUserWithExtendedSessionError

    return UserWithExtendedSession(
        session=extended(session, current_time=current_time),
    )
