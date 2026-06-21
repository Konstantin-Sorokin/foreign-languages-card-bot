from unittest.mock import AsyncMock

import pytest


class TestProgressService:
    @pytest.mark.parametrize(
        ("user_id", "original", "translation", "example", "example_translation"),
        [
            (1, "Car", "Машина", "I have a car", "У меня есть машина"),
            (2, "Apple", "Яблоко", "", ""),
        ],
    )
    async def test_create_progress(
        self,
        user_id,
        original,
        translation,
        example,
        example_translation,
        progress_service,
    ):
        """Проверяет создание карточки прогресса.

        Убеждается, что сервис формирует корректный POST-запрос с полным набором
        данных или с пустыми опциональными полями (примерами).
        """
        progress_service._request = AsyncMock()
        await progress_service.create_progress(
            user_id=user_id,
            original=original,
            translation=translation,
            example=example,
            example_translation=example_translation,
        )

        progress_service._request.assert_awaited_once_with(
            method="POST",
            endpoint=f"users/{user_id}/progress/",
            json={
                "original": original,
                "translation": translation,
                "example": example,
                "example_translation": example_translation,
            },
        )

    @pytest.mark.parametrize(
        ("user_id", "card_id", "success"),
        [
            (1, 1, False),
            (1, 2, False),
            (1, 2, True),
            (2, 5, True),
        ],
    )
    async def test_update_progress(self, user_id, card_id, success, progress_service):
        """Проверяет обновление статуса знания карточки.

        Убеждается, что сервис отправляет PATCH-запрос с правильным ID карточки
        и булевым флагом успеха (success).
        """
        progress_service._request = AsyncMock()
        await progress_service.update_progress(
            user_id=user_id, card_id=card_id, success=success
        )

        progress_service._request.assert_awaited_once_with(
            method="PATCH",
            endpoint=f"users/{user_id}/card/{card_id}/progress/",
            json={
                "success": success,
            },
        )
