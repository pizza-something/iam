from dataclasses import dataclass
from typing import Any

from iam.application.errors.access import NotAuthenticatedError
from iam.application.ports.clock import Clock
from iam.application.ports.expiring_token_encoding import (
    ExpiringTokenEncoding,
)
from iam.entities.access.session import (
    NotExtendableSessionForExtendedSessionError,
    Session,
)
from iam.entities.access.token import AccessToken, RefreshToken
from iam.entities.access.user import (
    NotActiveSessionForUserWithExtendedSessionError,
    user_with_extended_session_when,
)


@dataclass(kw_only=True, frozen=True, slots=True)
class Output[EncodedAccessTokenT, EncodedRefreshTokenT]:
    encoded_access_token: EncodedAccessTokenT
    encoded_refresh_token: EncodedRefreshTokenT


@dataclass(kw_only=True, frozen=True, slots=True)
class ExtendSession[
    EncodedAccessTokenT = Any,
    EncodedRefreshTokenT = Any,
]:
    clock: Clock
    access_token_encoding: ExpiringTokenEncoding[
        AccessToken, EncodedAccessTokenT
    ]
    refresh_token_encoding: ExpiringTokenEncoding[
        RefreshToken, EncodedRefreshTokenT
    ]

    async def __call__(
        self,
        encoded_access_token: EncodedAccessTokenT | None,
        encoded_refresh_token: EncodedRefreshTokenT | None,
    ) -> Output[EncodedAccessTokenT, EncodedRefreshTokenT]:
        """
        :raises iam.application.errors.access.NotAuthenticatedError:
        """

        if encoded_access_token is None or encoded_refresh_token is None:
            raise NotAuthenticatedError

        current_time = await self.clock.get_current_time()

        access_token = await self.access_token_encoding.decoded(
            encoded_access_token,
        )
        refresh_token = await self.refresh_token_encoding.decoded(
            encoded_refresh_token,
        )

        if access_token is None or refresh_token is None:
            raise NotAuthenticatedError

        session = Session(
            access_token=access_token,
            refresh_token=refresh_token,
        )

        try:
            user = user_with_extended_session_when(
                current_time=current_time,
                session=session,
            )
        except NotActiveSessionForUserWithExtendedSessionError as error:
            raise NotAuthenticatedError from error
        except NotExtendableSessionForExtendedSessionError as error:
            raise NotAuthenticatedError from error

        encoded_access_token = await self.access_token_encoding.encoded(
            user.session.access_token
        )
        encoded_refresh_token = await self.refresh_token_encoding.encoded(
            user.session.refresh_token
        )
        return Output(
            encoded_access_token=encoded_access_token,
            encoded_refresh_token=encoded_refresh_token,
        )
