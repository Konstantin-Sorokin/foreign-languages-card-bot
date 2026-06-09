import json
import random

from bot.services import BaseService
from bot.utils import RedisKeys


class PackService(BaseService):
    async def get_packs(self) -> list:
        """
        Возвращает мета-информацию о всех доступных паках (ID и названия).

        - Проверяет наличие кэша в Redis по ключу 'packs:list'.
        - Если кэш отсутствует или истек, автоматически запускает
        синхронизацию данных из БД (_sync_verbs_and_packs_to_redis).
        """
        cached = await self.redis.get(RedisKeys.packs_list())

        if not cached:
            await self._sync_verbs_and_packs_to_redis()
            cached = await self.redis.get(RedisKeys.packs_list())

        return json.loads(cached)

    async def get_verb(self, telegram_id: int) -> dict | None:
        """
        Извлекает следующий глагол из личной очереди пользователя.
        Использует команду LPOP, что гарантирует удаление элемента из очереди при получении
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
        1. Проверка кэша: если данные паков отсутствуют в Redis, берет из БД
        2. Собирает все глаголы из указанных pack_ids в единый список.
        3. Рандомизация: перемешивает список и отбирает определенное кол-во карт(AMOUNT_VERB).
        4. Запись: сохраняет результат в личную очередь пользователя с TTL.
        """

        TTL = 60 * 60  # 1 час
        AMOUNT_VERB = 40

        if not await self.redis.exists(RedisKeys.pack_verbs(pack_ids[0])):
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
        Выполняет полную синхронизацию данных из БД в Redis.

        Загружает список всех паков и их содержимое (глаголы с примерами).
        Устанавливает длительное время жизни (15 дней) для снижения нагрузки на БД.
        Использует Pipeline для атомарной и быстрой записи данных.
        """

        TIME = 60 * 60 * 24 * 15  # 15 дней

        packs = await self._request(method="GET", endpoint="packs/")
        await self.redis.set(
            RedisKeys.packs_list(),
            json.dumps(packs, ensure_ascii=False),
            ex=TIME,
        )

        for pack in packs:
            pack_id = pack["id"]

            verbs = await self._request("GET", f"packs/{pack_id}/cards/")
            queue_key = RedisKeys.pack_verbs(pack_id)
            pipe = self.redis.pipeline()
            await pipe.delete(queue_key)

            for verb in verbs:
                pipe.rpush(queue_key, json.dumps(verb, ensure_ascii=False))

            await pipe.expire(queue_key, TIME)
            await pipe.execute()
