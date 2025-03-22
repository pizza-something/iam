from dataclasses import dataclass

from effect import Effect, just

from iam.entities.access.access_token import (
    AccessToken,
    new_access_token_when,
    refreshed,
)
from iam.entities.access.account import (
    Account,
    AccountName,
    registered_account_when,
)
from iam.entities.access.expiring_token import InvalidTokenError, valid
from iam.entities.access.password import Password, PasswordHashing
from iam.entities.access.refresh_token import (
    RefreshToken,
    new_refreh_token_when,
)
from iam.entities.time.time import Time


@dataclass(kw_only=True, frozen=True)
class SignedUpUser:
    refresh_token: RefreshToken
    access_token: AccessToken


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
    signed_up_user = SignedUpUser(
        refresh_token=new_refreh_token_when(
            current_time=current_time, account_id=just(account).id
        ),
        access_token=new_access_token_when(
            current_time=current_time, account_id=just(account).id
        )
    )
    return account.map(lambda _: signed_up_user)


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
    refresh_token: RefreshToken
    access_token: AccessToken


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

    return SignedInUser(
        refresh_token=new_refreh_token_when(
            current_time=current_time, account_id=account.id
        ),
        access_token=new_access_token_when(
            current_time=current_time, account_id=account.id
        )
    )


@dataclass(kw_only=True, frozen=True)
class UserWithRefreshedAccessToken:
    access_token: AccessToken


def user_with_refreshed_access_token_when(
    *,
    current_time: Time,
    refresh_token: RefreshToken | None,
    access_token: AccessToken | None,
) -> UserWithRefreshedAccessToken:
    """
    :raises iam.entities.access.token.InvalidTokenError:
    """

    if access_token is None:
        raise InvalidTokenError

    refresh_token = valid(refresh_token, current_time=current_time)
    access_token = refreshed(access_token, current_time=current_time)

    return UserWithRefreshedAccessToken(access_token=access_token)
