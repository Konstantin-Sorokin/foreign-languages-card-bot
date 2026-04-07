class RedisKeys:
    @staticmethod
    def user_id(telegram_id: int) -> str:
        return f"user:{telegram_id}:id"

    @staticmethod
    def user_cards(telegram_id: int) -> str:
        return f"user:{telegram_id}:cards"

    @staticmethod
    def user_verbs(telegram_id: int) -> str:
        return f"user:{telegram_id}:verbs"

    @staticmethod
    def user_index(telegram_id: int) -> str:
        return f"user:{telegram_id}:index"

    @staticmethod
    def packs() -> str:
        return "packs"
