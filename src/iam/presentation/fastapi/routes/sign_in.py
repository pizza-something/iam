from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel

from iam.application.errors.access import NotAuthenticatedError
from iam.application.sign_in import SignIn
from iam.infrastructure.pydantic.schemas.common import NoDataSchema
from iam.presentation.fastapi.cookies import (
    AccessTokenCookie,
    RefreshTokenCookie,
)
from iam.presentation.fastapi.fields import name_field, password_field
from iam.presentation.fastapi.schemas.errors import (
    NotAuthenticatedSchema,
    ErrorListSchema,
)
from iam.presentation.fastapi.tags import Tag


sign_in_router = APIRouter()


class SignInSchema(BaseModel):
    name: str = name_field
    password: str = password_field


@sign_in_router.post(
    "/account/session",
    responses={
        status.HTTP_201_CREATED: {"model": NoDataSchema},
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorListSchema[NotAuthenticatedSchema]
        },
    },
    summary="Sign in",
    description="Create a new session for a current user.",
    tags=[Tag.user, Tag.account, Tag.session],
)
@inject
async def sign_in_route(
    sign_in: FromDishka[SignIn[str, str]],
    request_body: SignInSchema,
) -> Response:
    response_body_model: BaseModel

    try:
        output = await sign_in(
            request_body.name,
            request_body.password,
        )
    except NotAuthenticatedError:
        response_body_model = NotAuthenticatedSchema().to_list()
        response_body = response_body_model.model_dump(by_alias=True)
        status_code = status.HTTP_401_UNAUTHORIZED
        return JSONResponse(response_body, status_code=status_code)

    response = JSONResponse({}, status_code=status.HTTP_201_CREATED)

    access_token_cookie = AccessTokenCookie(response)
    refresh_token_cookie = RefreshTokenCookie(response)

    access_token_cookie.set(output.encoded_access_token)
    refresh_token_cookie.set(output.encoded_refresh_token)

    return response
