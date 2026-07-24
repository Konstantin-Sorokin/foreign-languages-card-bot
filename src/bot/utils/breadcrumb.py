from bot.schemas.pack import BreadcrumbPack
from bot.utils.constants import PACK_KIND_ICONS


def get_breadcrumb_path(path: list[int]) -> list[int]:
    """Remove the root element from the breadcrumb path."""
    if len(path) <= 1:
        return path

    return path[1:]


def build_breadcrumb_text(packs: list[BreadcrumbPack]) -> str:
    """Build a formatted breadcrumb string with icons and names."""
    return "\n".join(f"{PACK_KIND_ICONS[pack.kind]} {pack.name}" for pack in packs)
