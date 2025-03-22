from dataclasses import dataclass
from datetime import timedelta
from uuid import UUID

from iam.entities.access.expiring_token import ExpiringToken
from iam.entities.time.time import Time


@dataclass(kw_only=True, frozen=True)
class RefreshToken(ExpiringToken):
    account_id: UUID


def new_refreh_token_when(
    *,
    current_time: Time,
    account_id: UUID,
) -> RefreshToken:
    return RefreshToken(
        account_id=account_id,
        expiration_time=current_time.map(lambda it: it + timedelta(days=365)),
    )
