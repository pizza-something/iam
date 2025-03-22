from dataclasses import dataclass

from iam.entities.time.time import Time


@dataclass(kw_only=True, frozen=True)
class ExpiringToken:
    expiration_time: Time


def is_expired(
    refresh_token: ExpiringToken, *, current_time: Time
) -> bool:
    return refresh_token.expiration_time <= current_time


class InvalidTokenError(Exception): ...


def valid[TokenT: ExpiringToken](
    token: TokenT | None,
    *,
    current_time: Time,
) -> TokenT:
    """
    :raises iam.entities.access.token.InvalidTokenError:
    """

    if token is None:
        raise InvalidTokenError

    if is_expired(token, current_time=current_time):
        raise InvalidTokenError

    return token
