from fastapi.security import OAuth2PasswordRequestForm
from typing import Union
from pydantic import BaseModel, Field
from typing_extensions import Annotated
from fastapi.param_functions import Form


class TokenSchema(BaseModel):
    access_token: str
    token_type: str


class TokenDataSchema(BaseModel):
    id: int = Field(default=None)
    scopes: list[str] = []


