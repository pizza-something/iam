from typing import Literal, Self

from pydantic import BaseModel, Field


class ErrorListSchema[ErrorSchemaT](BaseModel):
    error_models: tuple[ErrorSchemaT] = Field(alias="errors")


class ErrorSchema(BaseModel):
    def to_list(self) -> ErrorListSchema[Self]:
        return ErrorListSchema(errors=(self,))


class EmptyAccountNameSchema(ErrorSchema):
    type: Literal["emptyAccountName"] = "emptyAccountName"


class AccountNameTakenSchema(ErrorSchema):
    type: Literal["accountNameTaken"] = "accountNameTaken"


class ShortPasswordSchema(ErrorSchema):
    type: Literal["shortPassword"] = "shortPassword"


class NotAuthenticatedSchema(ErrorSchema):
    type: Literal["notAuthenticated"] = "notAuthenticated"
