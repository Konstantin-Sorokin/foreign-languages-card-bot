from pydantic import BaseModel


class UserRead(BaseModel):
    id: int
    telegram_id: int


class UserProgressUpdate(BaseModel):
    user_id: int
    success: bool


class UserCreate(BaseModel):
    telegram_id: int
