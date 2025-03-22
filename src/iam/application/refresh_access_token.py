from dataclasses import dataclass
from typing import Any

from iam.application.errors.access_denied_error import AccessDeniedError
from iam.application.ports.accounts import Accounts
from iam.application.ports.clock import Clock
from iam.application.ports.expiring_token_encoding import (
    ExpiringTokenEncoding,
)
from iam.entities.access.access_token import AccessToken
from iam.entities.access.expiring_token import InvalidTokenError
from iam.entities.access.password import PasswordHashing
from iam.entities.access.refresh_token import RefreshToken
from iam.entities.access.user import user_with_refreshed_access_token_when


@dataclass(kw_only=True, frozen=True, slots=True)
class Output[EncodedAccessTokenT]:
    encoded_access_token: EncodedAccessTokenT


@dataclass(kw_only=True, frozen=True, slots=True)
class RefreshAccessToken[
    EncodedAccessTokenT = Any,
    EncodedRefreshTokenT = Any,
    AccountsT: Accounts = Accounts,
]:
    clock: Clock
    access_token_encoding: ExpiringTokenEncoding[
        AccessToken, EncodedAccessTokenT
    ]
    refreh_token_encoding: ExpiringTokenEncoding[
        RefreshToken, EncodedRefreshTokenT
    ]
    password_hashing: PasswordHashing

    async def __call__(
        self,
        encoded_access_token: EncodedAccessTokenT,
        encoded_refresh_token: EncodedRefreshTokenT,
    ) -> Output[EncodedAccessTokenT]:
        """
        :raises iam.apploication.errors.access_denied_error.AccessDeniedError:
        """

        current_time = await self.clock.get_current_time()

        access_token = await self.access_token_encoding.decoded(
            encoded_access_token,
        )
        refresh_token = await self.refreh_token_encoding.decoded(
            encoded_refresh_token,
        )

        try:
            user = user_with_refreshed_access_token_when(
                current_time=current_time,
                access_token=access_token,
                refresh_token=refresh_token,
            )
        except InvalidTokenError as error:
            raise AccessDeniedError from error

        encoded_access_token = await self.access_token_encoding.encoded(
            user.access_token
        )
        return Output(encoded_access_token=encoded_access_token)
