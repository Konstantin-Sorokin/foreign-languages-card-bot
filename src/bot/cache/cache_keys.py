class CacheKey:
    @staticmethod
    def user_db_id(telegram_id: int) -> str:
        """Redis key for user's database ID."""
        return f"user:{telegram_id}:id"

    @staticmethod
    def user_cards(user_id: int):
        """Redis key for user's card queue."""
        return f"user:{user_id}:cards"

    @staticmethod
    def current_card(user_id: int):
        """Redis key for the card currently being reviewed."""
        return f"user:{user_id}:current_card"

    @staticmethod
    def user_verbs(user_id: int):
        """Redis key for user's irregular verbs queue."""
        return f"user:{user_id}:verbs"

    @staticmethod
    def current_verb(user_id: int):
        """Redis key for the verb currently being studied."""
        return f"user:{user_id}:current_verb"
