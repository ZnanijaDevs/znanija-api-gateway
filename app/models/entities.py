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


class LegacyUserWithBasicData(BaseModel):
    nick: str
    id: BRAINLY_USER_ID
    is_deleted: bool
    avatar: str | None = None


class LegacyUser(LegacyUserWithBasicData):
    gender: int
    ranks: list[str]


class ModeratorInModeratorsList(BaseModel):
    id: BRAINLY_USER_ID
    avatar: str
    nick: str
    ranks: list[str]


class PlaceInModeratorsRanking(BaseModel):
    points: conint(gt=0)
    user_id: int
    user_nick: str
    user_ranks: list[str]


class ReportedContentsCountBySubject(BaseModel):
    subject_id: int
    count: int


class FeedNode(BaseModel):
    is_reported: bool
    content: str
    author: TransformedGraphqlUser
    id: int
    created: str
    attachments: list[str]
    subject: str | None
    subject_id: int | None
    answers: list["FeedNode"] | None
    is_best: bool | None
    is_confirmed: bool | None


class LegacyTaskNode(BaseModel):
    author: LegacyUser
    attachments: list[str]
    full_content: str
    filtered_content: str
    short_content: str
    has_attachments: bool
    created: str
    id: int
    is_deleted: bool
    is_reported: bool


class LegacyAnswer(LegacyTaskNode):
    is_best: bool
    is_approved: bool
    is_to_correct: bool


class LegacyQuestion(LegacyTaskNode):
    link: str
    points: int
    subject: str | None
    subject_id: int | None
    answers: list[LegacyAnswer]
    answers_count: int
    can_answer: bool


class DescriptionInEntryInTaskLog(TypedDict):
    text: str
    title: str


class EntryInTaskLog(BaseModel):
    text: str
    warn: bool
    type: str
    time: str
    date: str
    descriptions: list[DescriptionInEntryInTaskLog]
    owner: LegacyUser | None = None
    user: LegacyUser | None = None
