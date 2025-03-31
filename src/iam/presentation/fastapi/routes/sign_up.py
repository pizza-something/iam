from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel

from iam.application.ports.map import NotUniqueAccountNameError
from iam.application.sign_up import SignUp
from iam.entities.access.account import EmptyAccountNameError
from iam.entities.access.password import ShortPasswordError
from iam.infrastructure.pydantic.schemas.common import NoDataSchema
from iam.presentation.fastapi.cookies import (
    AccessTokenCookie,
    RefreshTokenCookie,
)
from iam.presentation.fastapi.fields import name_field, password_field
from iam.presentation.fastapi.schemas.errors import (
    EmptyAccountNameSchema,
    ErrorListSchema,
    NotUniqueAccountNameSchema,
    ShortPasswordSchema,
)
from iam.presentation.fastapi.tags import Tag


sign_up_router = APIRouter()


class SignUpSchema(BaseModel):
    name: str = name_field
    password: str = password_field


@sign_up_router.post(
    "/account",
    responses={
        status.HTTP_201_CREATED: {"model": NoDataSchema},
        status.HTTP_409_CONFLICT: {
            "model": ErrorListSchema[NotUniqueAccountNameSchema],
        },
        status.HTTP_400_BAD_REQUEST: {
            "model": (
                ErrorListSchema[EmptyAccountNameSchema]
                | ErrorListSchema[ShortPasswordSchema]
            ),
        },
    },
    summary="Sign up",
    description="Register an account of a current user.",
    tags=[Tag.user, Tag.account],
)
@inject
async def sign_up_route(
    sign_up: FromDishka[SignUp[str, str]],
    request_body: SignUpSchema,
) -> Response:
    response_body_model: BaseModel

    try:
        output = await sign_up(
            request_body.name,
            request_body.password,
        )
    except EmptyAccountNameError:
        response_body_model = EmptyAccountNameSchema().to_list()
        response_body = response_body_model.model_dump(by_alias=True)
        status_code = status.HTTP_400_BAD_REQUEST
        return JSONResponse(response_body, status_code=status_code)
    except ShortPasswordError:
        response_body_model = ShortPasswordSchema().to_list()
        response_body = response_body_model.model_dump(by_alias=True)
        status_code = status.HTTP_400_BAD_REQUEST
        return JSONResponse(response_body, status_code=status_code)
    except NotUniqueAccountNameError:
        response_body_model = NotUniqueAccountNameSchema().to_list()
        response_body = response_body_model.model_dump(by_alias=True)
        status_code = status.HTTP_409_CONFLICT
        return JSONResponse(response_body, status_code=status_code)

    response = JSONResponse({}, status_code=status.HTTP_201_CREATED)

    access_token_cookie = AccessTokenCookie(response)
    refresh_token_cookie = RefreshTokenCookie(response)

    access_token_cookie.set(output.encoded_access_token)
    refresh_token_cookie.set(output.encoded_refresh_token)

    return response
