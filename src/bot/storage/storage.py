from collections import defaultdict

from bot.schemas.irregular_verb import IrregularVerbRead
from bot.schemas.pack import PackStorageItem
from bot.utils.enums import VerbGroup


class Storage:
    def __init__(self):
        self.verbs_by_group: dict[VerbGroup, list[IrregularVerbRead]] = {}
        self.packs: dict[int, PackStorageItem] = {}
        self.pack_children: defaultdict[int | None, list[int]] = defaultdict(list)
