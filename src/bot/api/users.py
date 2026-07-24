from bot.api.base import BaseApiClient
from bot.schemas.user import UserCreate, UserRead


class UserApi(BaseApiClient):
    async def get_or_create(self, data: UserCreate) -> UserRead:
        """Find existing user or create a new one."""
        data = await self.post("users/", json=data.model_dump())
        return UserRead.model_validate(data)
