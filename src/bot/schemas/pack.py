from dataclasses import dataclass

from pydantic import BaseModel

from bot.utils.enums import ContentType, PackKind


class PackRead(BaseModel):
    id: int
    name: str
    parent_id: int | None
    order: int | None
    year: int | None
    kind: PackKind
    content_type: ContentType | None
    added: bool | None = None


class PackListResponse(BaseModel):
    packs: list[PackRead]


@dataclass
class PackStorageItem:
    id: int
    name: str
    parent_id: int | None
    order: int | None
    year: int | None
    kind: PackKind
    content_type: ContentType | None
