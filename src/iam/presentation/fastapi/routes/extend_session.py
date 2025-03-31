from typing import TYPE_CHECKING

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse, Response

from iam.application.errors.access import NotAuthenticatedError
from iam.application.extend_session import ExtendSession
from iam.infrastructure.pydantic.schemas.common import NoDataSchema
from iam.presentation.fastapi.cookies import (
    AccessTokenCookie,
    RefreshTokenCookie,
)
from iam.presentation.fastapi.schemas.errors import (
    ErrorListSchema,
    NotAuthenticatedSchema,
)
from iam.presentation.fastapi.tags import Tag


if TYPE_CHECKING:
    from pydantic import BaseModel


extend_session_router = APIRouter()


@extend_session_router.put(
    "/account/session",
    responses={
        status.HTTP_200_OK: {"model": NoDataSchema},
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorListSchema[NotAuthenticatedSchema]
        },
    },
    summary="Extend session",
    description="Make a current user session active again.",
    tags=[Tag.user, Tag.account, Tag.session],
)
@inject
async def extend_session_route(
    extend_session: FromDishka[ExtendSession[str, str]],
    encoded_access_token: AccessTokenCookie.StrOrNoneWithLock = None,
    encoded_refresh_token: RefreshTokenCookie.StrOrNoneWithLock = None,
) -> Response:
    response_body_model: BaseModel

    try:
        output = await extend_session(
            encoded_access_token,
            encoded_refresh_token,
        )
    except NotAuthenticatedError:
        response_body_model = NotAuthenticatedSchema().to_list()
        response_body = response_body_model.model_dump(by_alias=True)
        status_code = status.HTTP_401_UNAUTHORIZED
        return JSONResponse(response_body, status_code=status_code)

    response = JSONResponse({}, status_code=status.HTTP_200_OK)

    access_token_cookie = AccessTokenCookie(response)
    refresh_token_cookie = RefreshTokenCookie(response)

    access_token_cookie.set(output.encoded_access_token)
    refresh_token_cookie.set(output.encoded_refresh_token)

    return response
