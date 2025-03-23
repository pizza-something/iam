from dataclasses import dataclass
from datetime import timedelta
from uuid import UUID

from iam.entities.time.time import Time


@dataclass(kw_only=True, frozen=True)
class ExpiringToken:
    expiration_time: Time


def is_expired(
    refresh_token: ExpiringToken, *, current_time: Time
) -> bool:
    return refresh_token.expiration_time <= current_time


@dataclass(kw_only=True, frozen=True)
class AccessToken(ExpiringToken):
    account_id: UUID


def issued_access_token_when(
    *,
    current_time: Time,
    account_id: UUID,
) -> AccessToken:
    return AccessToken(
        account_id=account_id,
        expiration_time=current_time.map(lambda it: it + timedelta(minutes=15)),
    )


def refreshed(access_token: AccessToken, *, current_time: Time) -> AccessToken:
    return issued_access_token_when(
        current_time=current_time,
        account_id=access_token.account_id,
    )


@dataclass(kw_only=True, frozen=True)
class RefreshToken(ExpiringToken): ...


def issued_refresh_token_when(
    *,
    current_time: Time,
) -> RefreshToken:
    return RefreshToken(
        expiration_time=current_time.map(lambda it: it + timedelta(days=365)),
    )
