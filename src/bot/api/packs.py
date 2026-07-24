from bot.api.base import BaseApiClient
from bot.schemas.pack import PackListResponse, PackRead
from bot.schemas.translation_card import TranslationCardListAdapter, TranslationCardRead


class PackApi(BaseApiClient):
    async def get_all_packs(self) -> list[PackRead]:
        """Get all available packs."""
        data = await self.get("packs/")
        return PackListResponse.model_validate(data).packs

    async def open_pack(self, pack_id: int, user_id: int) -> PackListResponse:
        """Get pack contents with user's subscription status."""
        data = await self.get(f"packs/{pack_id}", params={"user_id": user_id})

        return PackListResponse.model_validate(data)

    async def get_cards_by_pack(self, pack_id: int) -> list[TranslationCardRead]:
        """Get all cards belonging to a pack."""
        data = await self.get(f"packs/{pack_id}/cards")
        return TranslationCardListAdapter.validate_python(data)

    async def add_pack(self, pack_id: int, user_id: int) -> None:
        """Subscribe user to a pack."""
        await self.post(f"packs/{pack_id}/add", params={"user_id": user_id})
