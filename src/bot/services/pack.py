from dataclasses import asdict

from bot.api.learning import LearningApi
from bot.api.packs import PackApi
from bot.schemas.pack import PackListResponse, PackRead, PackStorageItem
from bot.schemas.translation_card import TranslationCardRead
from bot.storage.storage import Storage
from bot.utils.enums import PackKind, VerbGroup


class PackService:
    def __init__(
        self, learning_api: LearningApi, pack_api: PackApi, storage: Storage
    ) -> None:

        self._learning_api = learning_api
        self._pack_api = pack_api
        self._storage = storage

    async def get_packs(
        self,
        user_id: int,
        pack_id: int | None = None,
    ) -> PackListResponse:
        """Get packs at the given level, either from local storage or from the API."""
        children_ids = self._storage.pack_children[pack_id]

        packs = [self._storage.packs[child_id] for child_id in children_ids]

        if not packs:
            return PackListResponse(packs=[])

        if packs[0].kind == PackKind.CATEGORY:
            return PackListResponse(
                packs=[self._storage_to_read(pack) for pack in packs]
            )

        if pack_id is None:
            raise ValueError("Root pack cannot contain SET children")

        return await self._pack_api.open_pack(pack_id=pack_id, user_id=user_id)

    def get_breadcrumbs(
        self,
        pack_id: int | None = None,
    ) -> list[PackStorageItem]:
        """Build the breadcrumb path from root to the given pack."""
        breadcrumbs = []

        while pack_id is not None:
            pack = self._storage.packs[pack_id]
            breadcrumbs.append(pack)
            pack_id = pack.parent_id

        breadcrumbs.reverse()

        return breadcrumbs

    async def get_cards_by_pack(self, pack_id: int) -> list[TranslationCardRead]:
        """Get all cards belonging to a specific pack."""
        return await self._pack_api.get_cards_by_pack(pack_id=pack_id)

    async def add_pack(self, pack_id: int, user_id: int) -> None:
        """Subscribe the user to a pack."""
        await self._pack_api.add_pack(pack_id=pack_id, user_id=user_id)

    async def verbs_by_group(self) -> None:
        """Load irregular verbs from the API and group them by conjugation type."""
        for group in VerbGroup:
            irregular_verbs = await self._learning_api.get_iv_by_group(group)
            self._storage.verbs_by_group[group] = irregular_verbs

    async def load_packs(self) -> None:
        """Load all packs from the API into local storage."""
        packs = await self._pack_api.get_all_packs()

        for pack in packs:
            storage_pack = PackStorageItem(
                id=pack.id,
                name=pack.name,
                parent_id=pack.parent_id,
                order=pack.order,
                year=pack.year,
                kind=pack.kind,
                content_type=pack.content_type,
            )

            self._storage.packs[storage_pack.id] = storage_pack
            self._storage.pack_children[storage_pack.parent_id].append(storage_pack.id)

        for children in self._storage.pack_children.values():
            children.sort(key=lambda pack_id: self._storage.packs[pack_id].order or 0)

    def get_parent_id(
        self,
        pack_id: int,
    ) -> int | None:
        """Get the parent pack ID for the given pack."""
        return self._storage.packs[pack_id].parent_id

    @staticmethod
    def _storage_to_read(
        pack: PackStorageItem,
    ) -> PackRead:
        """Convert a storage pack item to an API response model."""
        return PackRead(**asdict(pack))
