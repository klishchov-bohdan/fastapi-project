from typing import Any

import pydantic
from pydantic import BaseModel, Field, validator
from typing_extensions import Annotated
from fastapi.param_functions import Form


class UserSchema(BaseModel):
    id: int = Field(default=None)
    username: str = Field(default=None)
    email: str | None
    disabled: bool = Field(default=False)
    verified: bool = Field(default=False)
    is_admin: bool = Field(default=False)


class UserRegistrationForm(BaseModel):
    username: Annotated[str, Form()] = Field(default=None)
    email: Annotated[pydantic.EmailStr, Form()] = Field(default=None)
    password: Annotated[str, Form()] = Field(default=None)


class UserEmailUpdateForm(BaseModel):
    new_email: Annotated[pydantic.EmailStr, Form()] = Field(default=None)


class UserNameUpdateForm(BaseModel):
    new_username: Annotated[str, Form()] = Field(default=None)


class UserPasswordUpdateForm(BaseModel):
    password: Annotated[str, Form()] = Field(default=None)
    new_password: Annotated[str, Form()] = Field(default=None)
