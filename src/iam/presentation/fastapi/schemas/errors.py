from typing import Literal, Self

from pydantic import BaseModel, Field


class ErrorListSchema[ErrorSchemaT](BaseModel):
    error_models: tuple[ErrorSchemaT] = Field(alias="errors")


class ErrorSchema(BaseModel):
    def to_list(self) -> ErrorListSchema[Self]:
        return ErrorListSchema(errors=(self,))


class EmptyAccountNameSchema(ErrorSchema):
    type: Literal["emptyAccountName"] = "emptyAccountName"


class NotUniqueAccountNameSchema(ErrorSchema):
    type: Literal["notUniqueAccountName"] = "notUniqueAccountName"


class ShortPasswordSchema(ErrorSchema):
    type: Literal["shortPassword"] = "shortPassword"


class AccessDeniedSchema(ErrorSchema):
    type: Literal["accessDenied"] = "accessDenied"
