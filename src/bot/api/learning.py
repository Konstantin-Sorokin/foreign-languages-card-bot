from bot.api.base import BaseApiClient
from bot.schemas.irregular_verb import IrregularVerbRead, irregular_verb_list_adapter
from bot.schemas.translation_card import TranslationCardListAdapter, TranslationCardRead
from bot.schemas.user import UserProgressUpdate
from bot.utils.enums import VerbGroup


class LearningApi(BaseApiClient):
    async def get_due_cards(self, user_id: int) -> list[TranslationCardRead]:
        """Get cards due for review."""
        data = await self.get(f"learning/{user_id}/due")
        return TranslationCardListAdapter.validate_python(data)

    async def update_progress(self, card_id: int, data: UserProgressUpdate) -> None:
        """Report learning result for a card."""
        await self.patch(f"learning/cards/{card_id}", json=data.model_dump())

    async def get_iv_by_group(self, group: VerbGroup) -> list[IrregularVerbRead]:
        """Get irregular verbs by their conjugation group."""
        data = await self.get("learning/irregular-verbs", params={"group": group.value})
        return irregular_verb_list_adapter.validate_python(data)

    async def get_random_iv(self) -> list[IrregularVerbRead]:
        """Get random irregular verbs for mixed practice."""
        data = await self.get("learning/irregular-verbs/random")
        return irregular_verb_list_adapter.validate_python(data)
