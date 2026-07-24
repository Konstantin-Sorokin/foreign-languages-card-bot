import logging
import random

from bot.api.learning import LearningApi
from bot.cache.cache_keys import CacheKey
from bot.cache.cache_service import CacheService
from bot.schemas.irregular_verb import IrregularVerbRead
from bot.schemas.translation_card import TranslationCardRead
from bot.schemas.user import UserProgressUpdate
from bot.storage.storage import Storage
from bot.utils.enums import VerbGroup

logger = logging.getLogger(__name__)


class LearningService:
    def __init__(
        self, cache: CacheService, learning_api: LearningApi, storage: Storage
    ) -> None:

        self._cache = cache
        self._learning_api = learning_api
        self._storage = storage

    async def process_answer(
        self,
        user_id: int,
        success: bool,
    ) -> TranslationCardRead | None:
        """Record the user's answer and return the next card to review."""
        await self.answer_card(user_id=user_id, success=success)

        return await self.get_next_card(user_id=user_id)

    async def get_next_card(self, user_id: int) -> TranslationCardRead | None:
        key = CacheKey.user_cards(user_id)

        card_data = await self._cache.lpop(key)
        if card_data is None:
            await self._fill_queue(user_id)
            card_data = await self._cache.lpop(key)

        if card_data is None:
            return None

        card = TranslationCardRead.model_validate(card_data)

        await self._cache.set(
            CacheKey.current_card(user_id),
            card_data,
            ttl=3600,
        )

        return card

    async def answer_card(self, user_id: int, success: bool) -> None:
        """Report learning result and reschedule the card if the answer was wrong."""
        card_data = await self._cache.get(CacheKey.current_card(user_id))
        if card_data is None:
            return

        await self._learning_api.update_progress(
            card_id=card_data["id"],
            data=UserProgressUpdate(user_id=user_id, success=success),
        )

        if not success:
            await self._cache.append_list(CacheKey.user_cards(user_id), card_data)

        await self._cache.delete(CacheKey.current_card(user_id))

    async def get_current_card(
        self,
        user_id: int,
    ) -> TranslationCardRead | None:
        data = await self._cache.get(CacheKey.current_card(user_id))

        if data is None:
            return None

        return TranslationCardRead.model_validate(data)

    async def start_verbs(
        self, user_id: int, group: VerbGroup | None = None
    ) -> IrregularVerbRead | None:
        """Initialize a verb study session, optionally filtered by group."""
        await self._cache.delete(CacheKey.user_verbs(user_id))

        await self._fill_iv_queue(user_id, group)

        return await self.get_next_verb(user_id)

    async def get_next_verb(self, user_id: int) -> IrregularVerbRead | None:

        verb_data = await self._cache.lpop(CacheKey.user_verbs(user_id))

        if verb_data is None:
            return None

        await self._cache.set(
            CacheKey.current_verb(user_id),
            verb_data,
            ttl=3600,
        )

        return IrregularVerbRead.model_validate(verb_data)

    async def get_current_verb(
        self,
        user_id: int,
    ) -> IrregularVerbRead | None:
        data = await self._cache.get(CacheKey.current_verb(user_id))

        if data is None:
            return None

        return IrregularVerbRead.model_validate(data)

    async def _fill_queue(self, user_id: int) -> None:
        """Fetch due cards from the API and cache them in a Redis list."""

        cards = await self._learning_api.get_due_cards(user_id)

        if not cards:
            return

        await self._cache.push_list(
            CacheKey.user_cards(user_id),
            [card.model_dump() for card in cards],
            ttl=3600,
        )

    async def _fill_iv_queue(self, user_id: int, group: VerbGroup | None) -> None:
        """Load verbs into the cache queue, either from storage or from the API."""

        if group is not None:
            verbs = self._storage.verbs_by_group[group].copy()
            random.shuffle(verbs)
        else:
            verbs = await self._learning_api.get_random_iv()

        await self._cache.push_list(
            CacheKey.user_verbs(user_id),
            [verb.model_dump() for verb in verbs],
            ttl=3600,
        )
