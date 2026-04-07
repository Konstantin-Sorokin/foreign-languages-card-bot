from bot.services import BaseService


class ProgressService(BaseService):
    async def create_progress(
        self, user_id: int, original: str, translation: str
    ) -> None:
        return await self._request(
            method="POST",
            endpoint=f"users/{user_id}/progress/",
            json={
                "original": original,
                "translation": translation,
            },
        )

    async def update_progress(self, user_id: int, card_id: int, success: bool) -> None:
        return await self._request(
            method="PATCH",
            endpoint=f"users/{user_id}/card/{card_id}/progress/",
            json={
                "success": success,
            },
        )
