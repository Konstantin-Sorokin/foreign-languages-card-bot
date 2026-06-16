import json
import random

from bot.services import BaseService
from bot.utils import RedisKeys


class PackService(BaseService):
    async def get_packs(self) -> list:
        """
        Возвращает список всех доступных паков с их ID и названиями.

        Данные кэшируются в Redis. При отсутствии кэша автоматически загружает
        данные из API через _sync_verbs_and_packs_to_redis.
        """
        cached = await self.redis.get(RedisKeys.packs_list())

        if not cached:
            await self._sync_verbs_and_packs_to_redis()
            cached = await self.redis.get(RedisKeys.packs_list())

        if not cached:
            return []

        return json.loads(cached)

    async def get_verb(self, telegram_id: int) -> dict | None:
        """
        Извлекает следующий глагол из личной очереди пользователя (LPOP).

        Returns:
            Словарь с данными глагола или None, если очередь пуста.
        """
        verb = await self.redis.lpop(RedisKeys.user_verbs(telegram_id))

        if not verb:
            return None

        return json.loads(verb)

    async def initialize_user_queue(
        self, telegram_id: int, pack_ids: list[int]
    ) -> None:
        """
        Формирует случайную очередь глаголов для сессии обучения.

        Алгоритм:
        1. Проверяет кэш паков в Redis; при отсутствии загружает из API.
        2. Собирает все глаголы из указанных pack_ids.
        3. Перемешивает и отбирает определенное кол-во глаголов - AMOUNT_VERB.
        4. Сохраняет результат в личную очередь пользователя на время TTL.
        """
        TTL = 60 * 60  # 1 час
        AMOUNT_VERB = 40

        need_sync = False
        for pack_id in pack_ids:
            if not await self.redis.exists(RedisKeys.pack_verbs(pack_id)):
                need_sync = True
                break
        if need_sync:
            await self._sync_verbs_and_packs_to_redis()

        queue_key = RedisKeys.user_verbs(telegram_id)
        await self.redis.delete(queue_key)

        all_available_verbs = []
        for pack_id in pack_ids:
            cached_verbs = await self.redis.lrange(RedisKeys.pack_verbs(pack_id), 0, -1)
            parsed_verbs = [json.loads(v) for v in cached_verbs]
            all_available_verbs.extend(parsed_verbs)

        random.shuffle(all_available_verbs)
        session_pack = all_available_verbs[:AMOUNT_VERB]

        pipe = self.redis.pipeline()
        for verb in session_pack:
            pipe.rpush(queue_key, json.dumps(verb, ensure_ascii=False))

        await pipe.expire(queue_key, TTL)
        await pipe.execute()

    async def _sync_verbs_and_packs_to_redis(self) -> None:
        """
        Полная синхронизация данных из API в Redis.

        Загружает:
        - Список всех паков (кэшируется на время TTL)
        - Для каждого пака — список глаголов с формами и примерами (кэшируется на время TTL)
        """
        TTL = 60 * 60 * 24 * 15  # 15 дней

        packs = await self._request(method="GET", endpoint="packs/")
        await self.redis.set(
            RedisKeys.packs_list(),
            json.dumps(packs, ensure_ascii=False),
            ex=TTL,
        )

        for pack in packs:
            pack_id = pack["id"]

            verbs = await self._request("GET", f"packs/{pack_id}/cards/")
            queue_key = RedisKeys.pack_verbs(pack_id)
            pipe = self.redis.pipeline()
            await pipe.delete(queue_key)

            for verb in verbs:
                pipe.rpush(queue_key, json.dumps(verb, ensure_ascii=False))

            await pipe.expire(queue_key, TTL)
            await pipe.execute()
