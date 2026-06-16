from bot.services import BaseService


class ProgressService(BaseService):
    async def create_progress(
        self,
        user_id: int,
        original: str,
        translation: str,
        example: str = "",
        example_translation: str = "",
    ) -> None:
        """
        Создаёт новую карточку с переводом и (опционально) примерами для пользователя.

        Args:
            user_id: ID пользователя в системе API.
            original: Слово или фраза на оригинальном языке.
            translation: Перевод на родной язык.
            example: Пример использования (опционально).
            example_translation: Перевод примера (опционально).
        """
        return await self._request(
            method="POST",
            endpoint=f"users/{user_id}/progress/",
            json={
                "original": original,
                "translation": translation,
                "example": example,
                "example_translation": example_translation,
            },
        )

    async def update_progress(self, user_id: int, card_id: int, success: bool) -> None:
        """
        Обновляет прогресс изучения карточки после ответа пользователя.

        Args:
            user_id: ID пользователя в системе API.
            card_id: ID карточки.
            success: True — пользователь знает карточку, False — не знает.
        """
        return await self._request(
            method="PATCH",
            endpoint=f"users/{user_id}/card/{card_id}/progress/",
            json={
                "success": success,
            },
        )
