from pydantic import BaseModel, TypeAdapter


class TranslationCardCreate(BaseModel):
    original: str
    translation: str

    example: str | None = None
    example_translation: str | None = None


class TranslationCardRead(BaseModel):
    id: int
    original: str
    translation: str

    example: str | None = None
    example_translation: str | None = None


TranslationCardListAdapter = TypeAdapter(list[TranslationCardRead])
