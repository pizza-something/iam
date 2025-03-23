from collections.abc import Iterator

from fastapi import APIRouter

from iam.presentation.fastapi.routes.extend_session import (
    extend_session_router,
)
from iam.presentation.fastapi.routes.healthcheck import (
    healthcheck_router,
)
from iam.presentation.fastapi.routes.sign_in import (
    sign_in_router,
)
from iam.presentation.fastapi.routes.sign_up import (
    sign_up_router,
)


all_routers = (
    healthcheck_router,
    sign_up_router,
    sign_in_router,
    extend_session_router,
)


class UnknownRouterError(Exception): ...


def ordered(*routers: APIRouter) -> Iterator[APIRouter]:
    for router in all_routers:
        if router not in routers:
            raise UnknownRouterError

        yield router
