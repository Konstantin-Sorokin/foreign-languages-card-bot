class RedisKeys:
    @staticmethod
    def user_id(telegram_id: int) -> str:
        """Ключ для хранения ID пользователя из БД."""
        return f"user:{telegram_id}:id"

    @staticmethod
    def user_cards(telegram_id: int) -> str:
        """Ключ для очереди карточек пользователя (режим 'Мои карточки')."""
        return f"user:{telegram_id}:cards"

    @staticmethod
    def user_verbs(telegram_id: int) -> str:
        """Ключ для очереди неправильных глаголов пользователя."""
        return f"user:{telegram_id}:verbs"

    @staticmethod
    def pack_verbs(pack_id: int) -> str:
        """Ключ для кэша глаголов конкретного пака."""
        return f"pack:{pack_id}:verbs_cache"

    @staticmethod
    def packs_list() -> str:
        """Ключ для списка всех доступных паков."""
        return "packs:list"
