from dataclasses import dataclass
from typing import Any

from iam.application.errors.access import NotAuthenticatedError
from iam.application.ports.accounts import Accounts
from iam.application.ports.clock import Clock
from iam.application.ports.expiring_token_encoding import (
    ExpiringTokenEncoding,
)
from iam.application.ports.transaction import TransactionOf
from iam.entities.access.account import AccountName, EmptyAccountNameError
from iam.entities.access.password import (
    Password,
    PasswordHashing,
    ShortPasswordError,
)
from iam.entities.access.token import AccessToken, RefreshToken
from iam.entities.access.user import (
    InvalidPasswordForPrimaryAuthenticatedUserError,
    signed_in_user_when,
)


@dataclass(kw_only=True, frozen=True, slots=True)
class Output[EncodedAccessTokenT, EncodedRefreshTokenT]:
    encoded_access_token: EncodedAccessTokenT
    encoded_refresh_token: EncodedRefreshTokenT


@dataclass(kw_only=True, frozen=True, slots=True)
class SignIn[
    EncodedAccessTokenT = Any,
    EncodedRefreshTokenT = Any,
    AccountsT: Accounts = Accounts,
]:
    clock: Clock
    access_token_encoding: ExpiringTokenEncoding[
        AccessToken, EncodedAccessTokenT
    ]
    refresh_token_encoding: ExpiringTokenEncoding[
        RefreshToken, EncodedRefreshTokenT
    ]
    accounts: AccountsT
    transaction_of: TransactionOf[tuple[AccountsT]]
    password_hashing: PasswordHashing

    async def __call__(
        self,
        account_name_text: str,
        password_text: str,
    ) -> Output[EncodedAccessTokenT, EncodedRefreshTokenT]:
        """
        :raises iam.application.errors.access.NotAuthenticatedError:
        """

        current_time = await self.clock.get_current_time()

        try:
            account_name = AccountName(text=account_name_text)
        except EmptyAccountNameError as error:
            raise NotAuthenticatedError from error

        try:
            password = Password(text=password_text)
        except ShortPasswordError as error:
            raise NotAuthenticatedError from error

        async with self.transaction_of((self.accounts, )):
            account = await self.accounts.account_with_name(account_name)

        if account is None:
            raise NotAuthenticatedError

        try:
            signed_in_user = signed_in_user_when(
                current_time=current_time,
                password_hashing=self.password_hashing,
                password=password,
                account=account,
            )
        except InvalidPasswordForPrimaryAuthenticatedUserError as error:
            raise NotAuthenticatedError from error

        encoded_access_token = await self.access_token_encoding.encoded(
            signed_in_user.session.access_token
        )
        encoded_refresh_token = await self.refresh_token_encoding.encoded(
            signed_in_user.session.refresh_token
        )
        return Output(
            encoded_access_token=encoded_access_token,
            encoded_refresh_token=encoded_refresh_token,
        )
