from pydantic import BaseModel


class NotificationMessage(BaseModel):
    event: str
    telegram_id: int
