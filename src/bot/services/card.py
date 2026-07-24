from bot.api.cards import CardApi
from bot.schemas.translation_card import TranslationCardCreate


class CardService:
    def __init__(self, card_api: CardApi) -> None:
        self._card_api = card_api

    async def create(
        self,
        user_id: int,
        card_data: TranslationCardCreate,
    ) -> None:
        """Normalize and save a new translation card."""
        card_data = self._normalize(card_data)
        await self._card_api.create_translation_card(data=card_data, user_id=user_id)

    def _normalize(self, card: TranslationCardCreate) -> TranslationCardCreate:
        """Normalize all text fields by collapsing whitespace."""
        return TranslationCardCreate(
            original=self._normalize_text(card.original),
            translation=self._normalize_text(card.translation),
            example=(
                self._normalize_text(card.example) if card.example is not None else None
            ),
            example_translation=(
                self._normalize_text(card.example_translation)
                if card.example_translation is not None
                else None
            ),
        )

    @staticmethod
    def _normalize_text(text: str) -> str:
        """Collapse multiple whitespace characters into a single space."""
        return " ".join(text.split())
