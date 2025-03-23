from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from uuid import UUID

import jwt as pyjwt

from iam.application.ports.expiring_token_encoding import ExpiringTokenEncoding
from iam.entities.access.token import AccessToken, ExpiringToken, RefreshToken
from iam.entities.time.time import NotUTCTimeError, Time
from iam.infrastructure.types import JWT


@dataclass(kw_only=True, frozen=True, slots=True)
class ExpiringTokenEncodingAsIdentification[TokenT: ExpiringToken](
    ExpiringTokenEncoding[TokenT, TokenT]
):
    async def encoded(
        self, token: TokenT, /
    ) -> TokenT:
        return token

    async def decoded(
        self, token: TokenT, /
    ) -> TokenT | None:
        return token


@dataclass(kw_only=True, frozen=True, slots=True)
class AccessTokenEncodingToHS256JWT(
    ExpiringTokenEncoding[AccessToken, JWT]
):
    secret: str = field(repr=False)

    async def encoded(self, token: AccessToken, /) -> JWT:
        payload = {"account_id": token.account_id}
        headers = {"exp": token.expiration_time.datetime.isoformat()}
        algorithm = "HS256"

        return pyjwt.encode(payload, self.secret, algorithm, headers)

    async def decoded(
        self, jwt: JWT, /
    ) -> AccessToken | None:
        try:
            data = pyjwt.decode_complete(jwt, self.secret, algorithms="HS256")
        except pyjwt.DecodeError:
            return None

        header: dict[str, Any] = data["header"]
        payload: dict[str, Any] = data["payload"]

        account_id_hex: Any = payload.get("account_id")
        expiration_iso_time: Any = header.get("exp")

        try:
            account_id = UUID(hex=account_id_hex)
        except ValueError:
            return None

        try:
            expiration_datetime = datetime.fromisoformat(expiration_iso_time)
        except ValueError:
            return None
        except TypeError:
            return None

        try:
            expiration_time = Time(datetime=expiration_datetime)
        except NotUTCTimeError:
            return None

        return AccessToken(
            account_id=account_id, expiration_time=expiration_time
        )


@dataclass(kw_only=True, frozen=True, slots=True)
class RefreshTokenEncodingToHS256JWT(
    ExpiringTokenEncoding[RefreshToken, JWT]
):
    secret: str = field(repr=False)

    async def encoded(self, token: RefreshToken, /) -> JWT:
        headers = {"exp": token.expiration_time.datetime.isoformat()}
        algorithm = "HS256"

        return pyjwt.encode({}, self.secret, algorithm, headers)

    async def decoded(
        self, jwt: JWT, /
    ) -> RefreshToken | None:
        try:
            data = pyjwt.decode_complete(jwt, self.secret, algorithms="HS256")
        except pyjwt.DecodeError:
            return None

        header: dict[str, Any] = data["header"]

        expiration_iso_time: Any = header.get("exp")

        try:
            expiration_datetime = datetime.fromisoformat(expiration_iso_time)
        except ValueError:
            return None
        except TypeError:
            return None

        try:
            expiration_time = Time(datetime=expiration_datetime)
        except NotUTCTimeError:
            return None

        return RefreshToken(expiration_time=expiration_time)
