from pydantic import BaseModel


class TransformedLegacyUserWithBasicData(BaseModel):
    nick: str
    id: int
    is_deleted: bool
    avatar: str | None = None


class TransformedGraphqlUser(BaseModel):
    created: str
    avatar: str
    nick: str
    id: int
    rank: str | None = None
    answers_count: int = 0
    answers_count_by_subject: list[dict[str, int]] = []
    has_special_ranks: bool = False
    special_ranks: list[str]
    gender: str
    is_deleted: bool
