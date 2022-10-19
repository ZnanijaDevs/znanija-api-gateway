from typing import Any
from pydantic import BaseModel

from .users import TransformedGraphqlUser


class TransformedFeedNode(BaseModel):
    is_reported: bool
    content: str
    author: TransformedGraphqlUser
    id: int
    created: str
    attachments: list[str]
    subject: str | None
    subject_id: int | None
    answers: list[Any] | None
    is_best: bool | None
    is_confirmed: bool | None
