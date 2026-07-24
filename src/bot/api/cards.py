from bot.api.base import BaseApiClient
from bot.schemas.translation_card import TranslationCardCreate


class CardApi(BaseApiClient):
    async def create_translation_card(
        self, user_id: int, data: TranslationCardCreate
    ) -> None:
        """Save a new translation card for the user."""
        await self.post("cards/", params={"user_id": user_id}, json=data.model_dump())
