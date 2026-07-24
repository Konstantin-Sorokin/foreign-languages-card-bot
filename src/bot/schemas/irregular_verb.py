from pydantic import BaseModel, TypeAdapter


class Verb(BaseModel):
    verb: str
    example: str
    example_translation: str


class IrregularVerbRead(BaseModel):
    id: int

    infinitive: Verb
    past_simple: Verb
    past_participle: Verb

    translation: str


irregular_verb_list_adapter = TypeAdapter(list[IrregularVerbRead])
