from typing import TypedDict, Any
from pydantic import BaseModel, conint


BRAINLY_USER_ID = conint(ge=1, lt=100_000_000_000)


class AnswersCountBySubject(TypedDict):
    count: int
    subject: str


class TransformedGraphqlUser(BaseModel):
    created: str
    avatar: str
    nick: str
    id: conint(ge=0, lt=1_000_000_000)
    rank: str | None = None
    answers_count: int = 0
    answers_count_by_subject: list[AnswersCountBySubject] = []
    has_special_ranks: bool = False
    special_ranks: list[str]
    gender: str
    is_deleted: bool


class TransformedLegacyUserWithBasicData(BaseModel):
    nick: str
    id: BRAINLY_USER_ID
    is_deleted: bool
    avatar: str | None = None


class ModeratorInModeratorsList(BaseModel):
    id: BRAINLY_USER_ID
    avatar: str
    nick: str
    ranks: list[str]


class PlaceInModeratorsRanking(BaseModel):
    place: conint(gt=0)
    points: conint(gt=0)
    user: TransformedGraphqlUser


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
