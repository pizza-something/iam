from pydantic import Field


name_field = Field(alias="name", min_length=1)
password_field = Field(alias="password", min_length=8, repr=False)
