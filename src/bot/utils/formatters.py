from bot.schemas.irregular_verb import IrregularVerbRead
from bot.schemas.pack import PackStorageItem
from bot.schemas.translation_card import TranslationCardCreate, TranslationCardRead
from bot.utils.constants import CONTENT_TYPE_ICONS
from bot.utils.enums import PackKind

DIVIDER = "•  •  •  •  •  •  •  •  •  •  •  •  •  •"
BREADCRUMBS_DIVIDER = "•  •  •  •  •  •  •  •  •  •  •  •  •  •  •  •  •  •  •"


def render_verb_front(verb: IrregularVerbRead) -> str:
    """Format the verb's infinitive for display."""
    return f"{DIVIDER}\n\n<b>{verb.infinitive.verb.upper()}</b>\n\n{DIVIDER}"


def render_verb_back(verb: IrregularVerbRead) -> str:
    """Format the full conjugation with examples for display."""
    return (
        f"{DIVIDER}\n\n"
        f"<b>"
        f"{verb.infinitive.verb.upper()} — "
        f"{verb.past_simple.verb.upper()} — "
        f"{verb.past_participle.verb.upper()}"
        f"</b>\n\n"
        f"<code>{verb.translation.upper()}</code>"
        f"\n\n{DIVIDER}\n\n"
        f"<b>Present:</b>\n"
        f"{verb.infinitive.example}\n"
        f"{verb.infinitive.example_translation}\n\n"
        f"<b>Past:</b>\n"
        f"{verb.past_simple.example}\n"
        f"{verb.past_simple.example_translation}\n\n"
        f"<b>Participle:</b>\n"
        f"{verb.past_participle.example}\n"
        f"{verb.past_participle.example_translation}"
        f"\n\n{DIVIDER}"
    )


def render_card_front(card: TranslationCardRead) -> str:
    """Format the card's original text for display."""
    return f"{DIVIDER}\n\n<b>{card.original.upper()}</b>\n\n{DIVIDER}"


def render_card_back(
    card: TranslationCardCreate | TranslationCardRead,
) -> str:
    """Format the card's translation and optional example for display."""
    text = f"{DIVIDER}\n\n"
    text += f"<b>{card.original.upper()}</b>\n"
    text += f"<code>{card.translation.upper()}</code>"

    if card.example:
        text += f"\n\n{DIVIDER}\n\n"
        text += f"<b>{card.example.upper()}</b>\n"
        if card.example_translation:
            text += f"<code>{card.example_translation.upper()}</code>"

    text += f"\n\n{DIVIDER}"

    return text


def render_pack_text(
    breadcrumbs: list[PackStorageItem],
) -> str:
    """Format the pack browser view with breadcrumb trail."""
    if not breadcrumbs:
        return "📁 Выберите категорию:"

    lines = [BREADCRUMBS_DIVIDER]

    for index, pack in enumerate(breadcrumbs):
        if pack.year is not None:
            lines.append(
                f"{'   ' * index}{get_pack_icon(pack)} {pack.name} ({pack.year})"
            )
        else:
            lines.append(f"{'   ' * index}{get_pack_icon(pack)} {pack.name}")
    lines.append(BREADCRUMBS_DIVIDER)
    return "\n".join(lines)


def get_pack_icon(pack: PackStorageItem) -> str:
    """Get the appropriate icon for a pack based on its kind and content type."""
    if pack.kind == PackKind.SET:
        return "📦"

    if pack.content_type:
        return CONTENT_TYPE_ICONS.get(pack.content_type, "📁")

    return "📁"
