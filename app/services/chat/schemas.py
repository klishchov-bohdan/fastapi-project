from pydantic import BaseModel, Field, validator
from typing_extensions import Annotated
from fastapi.param_functions import Form


class AnswerMessage(BaseModel):
    user_id: int
    message: str


class SendingMessage(BaseModel):
    message: Annotated[str, Form()] = Field(default=None)
