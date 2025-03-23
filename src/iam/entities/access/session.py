from dataclasses import dataclass
from uuid import UUID

from iam.entities.access.token import (
    AccessToken,
    RefreshToken,
    is_expired,
    issued_access_token_when,
    issued_refresh_token_when,
    refreshed,
)
from iam.entities.time.time import Time


@dataclass(kw_only=True, frozen=True)
class Session:
    access_token: AccessToken
    refresh_token: RefreshToken


def new_session_when(*, current_time: Time, account_id: UUID) -> Session:
    return Session(
        refresh_token=issued_refresh_token_when(current_time=current_time),
        access_token=issued_access_token_when(
            current_time=current_time, account_id=account_id
        ),
    )


def is_active(session: Session, *, current_time: Time) -> bool:
    return not is_expired(session.access_token, current_time=current_time)


def is_extendable(session: Session, *, current_time: Time) -> bool:
    return not is_expired(session.refresh_token, current_time=current_time)


class NotExtendableSessionForExtendedSessionError(Exception): ...


def extended(session: Session, *, current_time: Time) -> Session:
    """
    :raises iam.entities.access.session.NotExtendableSessionForExtendedSessionError:
    """  # noqa: E501

    if not is_extendable(session, current_time=current_time):
        raise NotExtendableSessionForExtendedSessionError

    return Session(
        access_token=refreshed(session.access_token, current_time=current_time),
        refresh_token=session.refresh_token,
    )
