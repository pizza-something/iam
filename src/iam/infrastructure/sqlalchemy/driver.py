from collections.abc import Sequence
from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession


@dataclass(kw_only=True, frozen=True, slots=True)
class PostgresDriver:
    session: AsyncSession


class ManyOrNoSessionsError(Exception): ...


def single_session_of(drivers: Sequence[PostgresDriver]) -> AsyncSession:
    sessions = set(driver.session for driver in drivers)

    if len(sessions) != 1:
        raise ManyOrNoSessionsError

    return sessions.pop()
